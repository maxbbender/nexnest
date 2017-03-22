from flask import Blueprint, render_template, request, jsonify

from nexnest.application import braintree, csrf

commerce = Blueprint('commerce', __name__, template_folder='../templates/commerce')


@commerce.route('/preCheckout', methods=['POST'])
def preCheckout():
    json = request.get_json(force=True)
    print(json)
    print("Items %r" % json['items'])
    print("Landlord ID %s" % json['landlord'])
    return jsonify({})


@commerce.route('/client_token', methods=['GET'])
def clientToken():
    token = braintree.ClientToken.generate()
    print(token)
    return token


@commerce.route('/checkout', methods=['GET'])
def checkout():
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
