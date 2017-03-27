from flask import Blueprint, render_template, request, jsonify

from pprint import pprint

from nexnest.application import braintree, csrf, session

from nexnest.models.transaction import ListingTransaction
from nexnest.models.listing import Listing

import json

commerce = Blueprint('commerce', __name__, template_folder='../templates/commerce')


# @commerce.route('/preCheckout', methods=['POST'])
# def preCheckout():
#     json = request.get_json(force=True)
#     print(json)
#     pprint(json['items'])
#     pprint("Landlord ID %s" % json['landlord'])

#     for item in json['items']:
#         print("Item %r" % item)
#         listing = session.query(Listing).filter_by(int(item['listing_id'])).first()
#         newListingTransaction = ListingTransaction(plan=item['plan'],
#                                                    listing=listing,
#                                                    status='new',
#                                                    success=False
#                                                    )

# return jsonify({})


@commerce.route('/client_token', methods=['GET'])
def clientToken():
    token = braintree.ClientToken.generate()
    print(token)
    return token


@commerce.route('/preCheckout', methods=['GET', 'POST'])
def viewPreCheckout():
    # testJson = {"landlord":1,"items":[{"listing_id":"2","plan":"standard"},{"listing_id":"3","plan":"premium"}]};
    jsonData = json.loads(request.form["json"])
    print("testJSON")
    pprint(jsonData)
    return render_template('confirmCheckout.html',
                           jsonData=jsonData)


@commerce.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout.html',
                           clientToken=braintree.ClientToken.generate())


# @commerce.route('/postListingCheckout', methods=['POST'])
# def postListingCheckout():
#     postedJSON = request.get_json(force=True)

#     for item in postedJSON['items']
#         newListingTransaction
#     pass


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
