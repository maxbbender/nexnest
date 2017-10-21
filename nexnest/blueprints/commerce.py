import json
from pprint import pformat

import braintree
from flask import current_app as app
from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
from nexnest import db
from nexnest.forms import PreCheckoutForm
from nexnest.models.coupon import Coupon
from nexnest.models.listing import Listing
from nexnest.models.transaction import (ListingTransaction,
                                        ListingTransactionListing)
from nexnest.utils.flash import flash_errors

session = db.session

commerce = Blueprint('commerce', __name__,
                     template_folder='../templates/commerce')


@commerce.route('/client_token', methods=['GET'])
@login_required
def clientToken():
    token = braintree.ClientToken.generate()
    print(token)
    return token


@commerce.route('/preCheckout', methods=['GET', 'POST'])
@login_required
def viewPreCheckout():
    form = PreCheckoutForm(request.form)

    if form.validate():
        jsonData = json.loads(request.form["json"])
        return render_template('confirmCheckout.html',
                               preCheckoutForm=PreCheckoutForm(),
                               jsonData=jsonData)
    else:
        return 'error'


@commerce.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    app.logger.debug('commerce.checkout() /checkout')
    if request.method == 'POST':
        form = PreCheckoutForm(request.form)

        if form.validate():
            listingObjects = json.loads(form.json.data)
            app.logger.debug('Form Validated')
            app.logger.debug('RAW Form JSON %s | Type %r' %
                             (form.json.data, type(form.json.data)))
            app.logger.debug('Parsed JSON %s | Type %r' %
                             (pformat(listingObjects), type(listingObjects)))

            # Create our transaction record
            newListingTransaction = ListingTransaction(user=current_user)
            session.add(newListingTransaction)
            session.commit()

            if 'couponCode' in listingObjects:
                couponCodeString = listingObjects['couponCode']

                # Lets check that the coupon is valid
                coupon = Coupon.query.filter_by(
                    coupon_key=couponCodeString).first()

                if coupon is not None:
                    if coupon.unlimited:
                        newListingTransaction.coupon_id = coupon.id
                        session.commit()
                    else:
                        if coupon.uses > 0:
                            newListingTransaction.coupon_id = coupon.id
                            coupon.uses = coupon.uses - 1
                            session.commit()
                        else:
                            app.logger.info(
                                '%r used coupon %r that has no uses left' % (current_user, coupon))
                else:
                    if couponCodeString != "":
                        app.logger.info(
                            'Coupon got passed through that is invalid. Code : %s' % couponCodeString)

            for item in listingObjects['items']:
                # Ambiguous variables because my database setup is stupid
                listing = session.query(Listing) \
                    .filter_by(id=int(item['listing_id'])) \
                    .first()
                newLTL = ListingTransactionListing(listing=listing,
                                                   listingTransaction=newListingTransaction,
                                                   plan=item['plan'])
                session.add(newLTL)
                session.commit()

            app.logger.debug("NewListingTransaction %r" %
                             newListingTransaction)
            app.logger.debug("NewListingTransaction LTL Objects %r" %
                             newListingTransaction.listings)

        else:
            app.logger.warning('Invalid PreCheckoutForm')
            flash_errors(form)

        return render_template('checkout.html',
                               clientToken=braintree.ClientToken.generate(),
                               totalPrice=newListingTransaction.totalTransactionPrice,
                               listingTransaction=newListingTransaction)
    else:
        if 'listingTransactionID' in request.args:
            listingTransaction = session.query(ListingTransaction) \
                .filter_by(id=int(request.args['listingTransactionID'])) \
                .first()

            if listingTransaction is not None:
                if listingTransaction.isViewableBy(current_user):
                    return render_template('checkout.html',
                                           clientToken=braintree.ClientToken.generate(),
                                           totalPrice=listingTransaction.totalTransactionPrice,
                                           listingTransaction=listingTransaction)


@commerce.route('/transactionGenerate', methods=['POST'])
def genTransaction():
    app.logger.debug('commerce.genTransaction() /transactionGenerate')

    listingTransaction = session.query(ListingTransaction) \
        .filter_by(id=int(request.form['listingTransactionID'])) \
        .first()

    if listingTransaction is not None:
        if listingTransaction.isViewableBy(current_user):

            transactionAmount = listingTransaction.totalTransactionPrice

            app.logger.debug('Generating Transaction for %r | Price %d | Nonce %s' % (
                listingTransaction, transactionAmount, request.form['payment_method_nonce']))

            result = None

            # Let's confirm the card
            # cardVerifResult = braintree.PaymentMethod.create({
            #     "customer_id": str(current_user.id),
            #     "payment_method_nonce": request.form['payment_method_nonce'],
            #     "options": {
            #         "verify_card": True
            #     }
            # })

            # if cardVerifResult.is_success:
            result = braintree.Transaction.sale({
                'amount': str(transactionAmount),
                'payment_method_nonce': request.form['payment_method_nonce'],
                'options': {
                    'submit_for_settlement': True
                }
            })

            if result.is_success or result.transaction:
                listingTransaction.success = True
                listingTransaction.status = result.transaction.status
                listingTransaction.braintree_transaction_id = result.transaction.id
                session.commit()

                # Now we want to go through the listings and set them to active
                app.logger.debug('Successfull Result')
                app.logger.debug("Setting these listings to active %r" %
                                 listingTransaction.listings)
                for ltl in listingTransaction.listings:
                    listing = ltl.listing
                    listing.active = True

                    ltl = ListingTransactionListing.query.filter_by(
                        listing=listing).first()

                    if ltl is not None:
                        if ltl.plan == 'premium':
                            listing.featured = True

                    session.commit()

                if request.is_xhr:
                    return jsonify({'success': True})
                else:
                    flash('Transaction Success, your listings are now live!', 'success')
                    return redirect(url_for('indexs.index'))

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
                    return redirect('/landlord/dashboard#checkoutTab')
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
        app.logger.warning("Could not find coupon with code %s" % couponCode)
        return jsonify(results={'validCoupon': False})
