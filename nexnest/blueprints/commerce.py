import datetime
import json
from pprint import pformat

from flask import current_app as app
from flask import (Blueprint, abort, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required

import braintree
from nexnest import db
from nexnest.forms import PreCheckoutForm, CheckoutForm
from nexnest.models.coupon import Coupon
from nexnest.models.listing import Listing
from nexnest.models.transaction import (ListingTransaction,
                                        ListingTransactionListing)
from nexnest.static.dataSets import schoolUpgradePrice, summerUpgradePrice
from nexnest.utils.flash import flash_errors, flash_errors_json
from nexnest.decorators import listing_transaction_viewable, listing_transaction_editable

session = db.session

commerce = Blueprint('commerce', __name__,
                     template_folder='../templates/commerce')


@commerce.route('/client_token', methods=['GET'])
@login_required
def clientToken():
    if current_user.braintree_customer_id:
        token = braintree.ClientToken.generate({'customer_id':current_user.braintree_customer_id})
    else:
        token = braintree.ClientToken.generate()

    if request.is_xhr:
        return jsonify({'token': token})
    else:
        return token


@commerce.route('/preCheckout', methods=['POST'])
@login_required
def viewPreCheckout():
    form = PreCheckoutForm()

    if form.validate_on_submit():
        jsonData = json.loads(form.json.data)

        app.logger.debug('Form Validated')
        app.logger.debug('RAW Form JSON %s | Type %r' %
                         (jsonData, type(jsonData)))
        app.logger.debug('Parsed JSON %s | Type %r' %
                         (pformat(jsonData), type(jsonData)))

        # Create our transaction record
        newListingTransaction = ListingTransaction(user=current_user)
        session.add(newListingTransaction)
        session.commit()

        if 'couponCode' in jsonData:
            couponCodeString = jsonData['couponCode']

            # Lets check that the coupon is valid
            coupon = Coupon.query.filter_by(coupon_key=couponCodeString).first()

            if coupon is not None:
                if coupon.unlimited:
                    newListingTransaction.coupon_id = coupon.id
                    session.commit()
                else:
                    if coupon.uses > 0:
                        newListingTransaction.coupon_id = coupon.id
                        session.commit()
                    else:
                        flash('Unable to apply coupon to purchase, it has not no uses left. Sorry!', 'warning')
                        app.logger.info('%r used coupon %r that has no uses left' % (current_user, coupon))
            else:
                if couponCodeString != "":
                    app.logger.info('Coupon got passed through that is invalid. Code : %s' % couponCodeString)

        for item in jsonData['items']:
            # Ambiguous variables because my database setup is stupid
            listing = session.query(Listing) \
                .filter_by(id=int(item['listing_id'])) \
                .first()

            if listing:
                newLTL = ListingTransactionListing(listing=listing,
                                                   listingTransaction=newListingTransaction,
                                                   plan=item['plan'])
                session.add(newLTL)
                session.commit()
            else:
                app.logger.warning('User tried to checkout a listing that does not exist: listing_id %r' % item['listing_id'])

        app.logger.debug("NewListingTransaction %r" %
                         newListingTransaction)
        app.logger.debug("NewListingTransaction LTL Objects %r" %
                         newListingTransaction.listings)

        return render_template('confirmCheckout.html',
                               preCheckoutForm=form,
                               jsonData=jsonData,
                               schoolUpgradePrice=schoolUpgradePrice,
                               summerUpgradePrice=summerUpgradePrice,
                               listingTransaction=newListingTransaction)
    else:
        flash_errors(form)
        app.logger.warning(form.errors)
        return form.redirect()


@commerce.route('/checkout/<int:listingTransactionID>', methods=['GET'])
@login_required
@listing_transaction_viewable
def checkout(listingTransactionID):
    checkoutForm = CheckoutForm()
    checkoutForm.listingTransactionID.data = listingTransactionID
    listingTransaction = ListingTransaction.query \
        .filter_by(id=listingTransactionID) \
        .first_or_404()

    return render_template('checkout2.html',
                           clientToken=braintree.ClientToken.generate(),
                           totalPrice=listingTransaction.totalTransactionPrice,
                           listingTransaction=listingTransaction,
                           form=checkoutForm)


@commerce.route('/transactionGenerate', methods=['POST'])
@login_required
def genTransaction():
    checkoutForm = CheckoutForm()

    if checkoutForm.validate_on_submit():
        listingTransaction = ListingTransaction.query.filter_by(id=checkoutForm.listingTransactionID.data).first_or_404()

    
        if listingTransaction.isViewableBy(current_user):

            transactionAmount = listingTransaction.totalTransactionPrice

            app.logger.debug('Generating Transaction for %r | Price %d | Nonce %s' % (
                listingTransaction, transactionAmount, checkoutForm.paymentMethodNonce.data))

            result = None

            # We need to create the customer record on braintree. First let's see if the customer already exists in their database

            # Search for a customer with the email of the user
            if current_user.braintree_customer_id:

                searchedCustomers = braintree.Customer.search(
                    braintree.CustomerSearch.id == current_user.braintree_customer_id
                )

                app.logger.debug('Seach Customer Result %r' % searchedCustomers.items)
                app.logger.debug(type(searchedCustomers))
                app.logger.debug(type(searchedCustomers.items))
            else:
                searchedCustomers = None

            

            foundCustomer = False
            customer = None

            if searchedCustomers:
                for customerItem in searchedCustomers.items:
                    if customerItem:
                        customer = customerItem
                        app.logger.debug('Seach Customer Result %r' % customerItem)
                        app.logger.debug('Seach Customer Result %r' % type(customerItem))
                # app.logger.debug('Seach Customer Result %r' % searchedCustomers.first())

            if not customer:
                # Customer Doesn't Exist
                customerResponse = braintree.Customer.create({
                    "first_name": current_user.fname,
                    "last_name": current_user.lname,
                    "email": current_user.email
                })

                if customerResponse.is_success:
                    customer = customerResponse.customer
                    app.logger.info('Customer %r has been created on braintree. ID %r' % (customer, customer.id))
                    current_user.braintree_customer_id = customer.id
                    db.session.commit()


            result = braintree.Transaction.sale({
                'amount': str(transactionAmount),
                'payment_method_nonce': checkoutForm.paymentMethodNonce.data,
                'customer_id': customer.id,
                'options': {
                    'submit_for_settlement': True,
                    'store_in_vault_on_success': True,
                }
            })

            if result.is_success:
                listingTransaction.success = True
                listingTransaction.status = result.transaction.status
                listingTransaction.braintree_transaction_id = result.transaction.id
                session.commit()

                # Now we want to go through the listings and set them to active
                app.logger.debug('Successfull Result')
                app.logger.debug("Setting these listings to active %r" %
                                 listingTransaction.listings)

                # Subtract Coupon
                if listingTransaction.coupon:
                    listingTransaction.coupon.uses = listingTransaction.coupon.uses - 1
                    session.commit()

                for ltl in listingTransaction.listings:
                    listing = ltl.listing
                    listing.featured = True

                    session.commit()

                    # We also want to delete all other listings with the same address that
                    # are inactive and for the same time period
                    # app.logger.debug("Trying to find other inactive listings with the same address")

                    # Listings with the same addresses
                    # otherListingsWithSameAddress = None
                    # if listing.property_type == 'apartment':
                    #     otherListingsWithSameAddress = session.query(Listing) \
                    #         .filter_by(street=listing.street,
                    #                    city=listing.city,
                    #                    state=listing.state,
                    #                    zip_code=listing.zip_code,
                    #                    apartment_number=listing.apartment_number,
                    #                    active=False
                    #                    ) \
                    #         .all()
                    # else:
                    #     otherListingsWithSameAddress = session.query(Listing) \
                    #         .filter_by(street=listing.street,
                    #                    city=listing.city,
                    #                    state=listing.state,
                    #                    zip_code=listing.zip_code,
                    #                    active=False
                    #                    ) \
                    #         .all()

                    # app.logger.debug("Other listings with the same address : %r" % otherListingsWithSameAddress)
                    # app.logger.debug("Determining which ones have conflicting dates")

                    # conflictingDates = False
                    # conflictingListings = []
                    # for otherListing in otherListingsWithSameAddress:

                    #     # Serialize the dates into python Date
                    #     otherListingStartDate = otherListing.start_date
                    #     otherListingEndDate = otherListing.end_date

                    #     # If the other listing starts before the end, and after the start (conflict)
                    #     if otherListingStartDate <= listing.end_date and otherListingStartDate >= listing.start_date:
                    #         app.logger.debug("Found a listing with conflicting dates : %r" % otherListing)
                    #         db.session.delete(otherListing)
                    #         conflictingDates = True

                    #     # If the other listing starts before the start but ends after the start (conflict)
                    #     elif otherListingStartDate <= listing.start_date and otherListingEndDate >= listing.start_date:
                    #         app.logger.debug("Found a listing with conflicting dates : %r" % otherListing)
                    #         db.session.delete(otherListing)
                    #         conflictingDates = True
                    #     else:
                    #         app.logger.debug("Listing %s does not have conflicting dates" % otherListing)

                    # if conflictingDates:
                    #     db.session.commit()

                if request.is_xhr:
                    return jsonify({'success': True})
                else:
                    flash('Transaction Success!', 'success')
                    return redirect(url_for('landlords.landlordDashboard'))

            # The Transaction was NOT successfull
            else:
                app.logger.warning('Unsuccessfull Result for Commerce Checkout')
                # app.logger.warning('Transaction Error %s' % result.transaction.status)
                for x in result.errors.deep_errors:
                    app.logger.warning('Error: %s: %s' % (x.code, x.message))

                if request.is_xhr:
                    return jsonify({'success': False, 'message': 'Transaction Error!'})
                else:
                    flash('Transaction Error! Please check your information and try again, if you believe this is an error on our end please let us know!', 'danger')
                    return redirect(url_for('commerce.checkout', listingTransactionID=listingTransaction.id))
            # else:
            #     verification = cardVerifResult.credit_card_verification
            #     if verification:
            #         app.logger.warning('Unsuccessfull Result for Card Verification : %r' % (verification.status))
            #     else:
            #         app.logger.warning('Unsucess Result for Card Verification but unknown why')

            #     if request.is_xhr:
            #         return jsonify({'success': False, 'message': 'Transaction Error!'})
            #     else:
            #         flash('Transaction Error! Please check your information and try again, if you believe this is an error on our end please let us know!', 'danger')
            #         return redirect('/landlord/dashboard#checkoutTab')

    else:
        if request.is_xhr:
            return jsonify({'success': False, 'message': flash_errors_json(checkoutForm)})
        else:
            flash_errors(checkoutForm)
            return checkoutForm.redirect()


@commerce.route('/coupon/<couponCode>/check', methods=['GET'])
@login_required
def checkCouponCode(couponCode):
    coupon = session.query(Coupon) \
        .filter_by(coupon_key=couponCode) \
        .first()

    if coupon is not None:
        app.logger.debug("Found Coupon %r" % coupon)
        return jsonify(results={'validCoupon': True, 'coupon': coupon.serialize})
    else:
        app.logger.info("Could not find coupon with code %s" % couponCode)
        return jsonify(results={'validCoupon': False})


@commerce.route('/listingTransaction/<int:listingTransactionID>/removeListing/<int:listingID>')
@login_required
@listing_transaction_editable
def removeListingFromTransaction(listingTransactionID, listingID):
    errors = False
    listingTransaction = ListingTransaction.query.filter_by(id=listingTransactionID).first_or_404()

    # Let's see if there is a LTL (Listing Transaction Listing) with the given ID
    ltlToCheck = ListingTransactionListing.query.filter_by(listing_id=listingID, listing_transactions_id=listingTransactionID).first()

    if ltlToCheck:
        listingTransaction.listings.remove(ltlToCheck)
        db.session.commit()
    else:
        app.logger.info('Unable to remove listing from transaction as it doesn\'t exists')
        errors = True

    if errors:
        return jsonify({'success': False})
    else:
        return jsonify({'success': True})
