from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from pprint import pprint, pformat

from nexnest import logger
from nexnest.application import braintree, csrf, session

from nexnest.models.transaction import ListingTransaction, ListingTransactionListing
from nexnest.models.listing import Listing
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

            # Now we want to build out the listings we are going to create
            # the transaction for
            # listings = []
            # checkoutTotal = 0
            # for item in listingObjects['items']:
            #     listingObject = {}

            #     listingObject['listing'] = listing
            #     listingObject['plan'] = item['plan']
            #     listings.append(listingObject)

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
            print('invalid form')
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
    # dicts = request.form
    # for key in dicts:
    #     print ('form key %r' % dicts[key])
    # print("Card Number %s" % request.form['card-number'])
    # print("CVV %s" % request.form['cvv'])
    # print("Expriation %s" % request.form['expiration-date'])
    logger.debug("Nonce %s" % request.form['payment_method_nonce'])

    result = braintree.Transaction.sale({
        'amount': '1.00',
        'payment_method_nonce': 'fake-valid-visa-nonce',
        'options': {
            'submit_for_settlement': True
        }
    })

    if result.is_success:
        logger.debug('Successfull Result')

        listingTransaction = session.query(ListingTransaction) \
            .filter_by(id=int(request.form['listingTransactionID'])) \
            .first()

        if listingTransaction is not None:
            if listingTransaction.isViewableBy(current_user):
                listingTransaction.success = True
                listingTransaction.status = result.transaction.status
                listingTransaction.braintree_transaction_id = result.transaction.id
                session.commit()
        return 'yay'
    else:
        logger.warning('Unsuccessfull Result')
        logger.warning('Transaction Status %s' % result.transaction.status)
        return 'boo'
