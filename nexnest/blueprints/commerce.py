from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import current_user

from pprint import pprint, pformat

from nexnest import logger, env
from nexnest.application import braintree, csrf, session

from nexnest.models.transaction import ListingTransaction, ListingTransactionListing
from nexnest.models.listing import Listing
from nexnest.models.cupon import Cupon

from nexnest.forms import PreCheckoutForm
from nexnest.utils.flash import flash_errors

import json

commerce = Blueprint('commerce', __name__, template_folder='../templates/commerce')


@commerce.route('/client_token', methods=['GET'])
def clientToken():
    token = braintree.ClientToken.generate()
    print(token)
    return token


@commerce.route('/preCheckout', methods=['GET', 'POST'])
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
def checkout():
    logger.debug('commerce.checkout() /checkout')
    if request.method == 'POST':
        form = PreCheckoutForm(request.form)

        if form.validate():
            listingObjects = json.loads(form.json.data)
            logger.debug('Form Validated')
            logger.debug('RAW Form JSON %s | Type %r' % (form.json.data, type(form.json.data)))
            logger.debug('Parsed JSON %s | Type %r' % (pformat(listingObjects), type(listingObjects)))

            # Create our transaction record
            newListingTransaction = ListingTransaction(user=current_user)
            session.add(newListingTransaction)
            session.commit()

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

            logger.debug("NewListingTransaction %r" % newListingTransaction)
            logger.debug("NewListingTransaction LTL Objects %r" % newListingTransaction.listings)

        else:
            logger.warning('Invalid PreCheckoutForm')
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
    logger.debug('commerce.genTransaction() /transactionGenerate')

    listingTransaction = session.query(ListingTransaction) \
        .filter_by(id=int(request.form['listingTransactionID'])) \
        .first()

    if listingTransaction is not None:
        if listingTransaction.isViewableBy(current_user):

            transactionAmount = listingTransaction.totalTransactionPrice

            logger.debug('Generating Transaction for %r | Price %d | Nonce %s' % (listingTransaction, transactionAmount, request.form['payment_method_nonce']))

            # If we are in development we are going to use the fake payment
            # setup for braintree
            result = None
            if env == 'development' or env == 'test':
                logger.debug('genTransaction() - DEVELOPMENT SETTINGS')

                result = braintree.Transaction.sale({
                    'amount': str(transactionAmount),
                    'payment_method_nonce': 'fake-valid-visa-nonce',
                    'options': {
                        'submit_for_settlement': True
                    }
                })
            else:
                logger.debug('genTransaction() - PRODUCTION SETTINGS')

                result = braintree.Transaction.sale({
                    'amount': str(transactionAmount),
                    'payment_method_nonce': request.form['payment_method_nonce'],
                    'options': {
                        'submit_for_settlement': True
                    }
                })

            # The Transaction was successfull
            if result.is_success:
                listingTransaction.success = True
                listingTransaction.status = result.transaction.status
                listingTransaction.braintree_transaction_id = result.transaction.id
                session.commit()

                # Now we want to go through the listings and set them to active
                for listing in listingTransaction.listings:
                    listing.active = True
                    session.commit()

                logger.debug('Successfull Result')
                flash('Transaction Success, your listings are now live!', 'success')
                return redirect(url_for('indexs.index'))

            # The Transaction was NOT successfull
            else:
                logger.warning('Unsuccessfull Result')
                logger.warning('Transaction Error %s (%s|%s)' % (result.transaction.status, result.transaction.processor_response_code, result.transaction.processor_response_text))
                flash('Transaction Error %s (%s|%s) Contact an administrator if you believe this is an error our our end.' % (result.transaction.status, result.transaction.processor_response_code, result.transaction.processor_response_text), 'error')
                return redirect('/landlord/dashboard#checkoutTab')


# @commmerce.route('/cupon/<cuponCode>/check', methods=['POST'])
# @login_required
# def checkCuponCode(cuponCode):
#     cupon = session.query(Cupon) \
#     .filter_by(cupon_code=cuponCode) \
#     .first()

#     if cupon is not None:
#         