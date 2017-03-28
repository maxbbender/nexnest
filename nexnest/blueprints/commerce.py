from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user

from pprint import pprint, pformat

from nexnest import logger
from nexnest.application import braintree, csrf, session

from nexnest.models.transaction import ListingTransaction
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
    logger.debug('Checkout Route')
    form = PreCheckoutForm(request.form)

    if form.validate():
        listingObjects = json.loads(form.json.data)
        logger.debug('Form Validated')
        logger.debug('RAW Form JSON %s | Type %r' % (form.json.data, type(form.json.data)))
        logger.debug('Parsed JSON %s | Type %r' % (pformat(listingObjects), type(listingObjects)))

        # Now we want to build out listing transactions
        checkoutTotal = 0
        for item in listingObjects['items']:
            listing = session.query(Listing) \
                .filter_by(id=int(item['listing_id'])) \
                .first()

            newListingTransaction = ListingTransaction(listing=listing,
                                                       plan=item['plan'],
                                                       user=current_user)
    else:
        print('invalid form')
        flash_errors(form)

    return render_template('checkout.html',
                           clientToken=braintree.ClientToken.generate())


@commerce.route('/transactionGenerate', methods=['POST'])
@csrf.exempt
def genTransaction():
    print("Genning Transaction")
    # dicts = request.form
    # for key in dicts:
    #     print ('form key %r' % dicts[key])
    # print("Card Number %s" % request.form['card-number'])
    # print("CVV %s" % request.form['cvv'])
    # print("Expriation %s" % request.form['expiration-date'])
    print("Nonce %s" % request.form['payment_method_nonce'])

    result = braintree.Transaction.sale({
        'amount': '1.00',
        'payment_method_nonce': 'fake-valid-visa-nonce',
        'options': {
            'submit_for_settlement': True
        }
    })
    return result
