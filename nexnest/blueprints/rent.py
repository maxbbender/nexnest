from flask import Blueprint, render_template, request

from flask_login import login_required

from nexnest.decorators import rent_editable, rent_viewable
from nexnest.models.rent import Rent

from nexnest.application import session, braintree


rents = Blueprint('rents', __name__, template_folder='../templates/rents')


@rents.route('/rent/<rentID>/completed')
@login_required
@rent_editable
def markCompleted(rentID):
    rent = Rent.query.filter_by(id=rentID).first()

    rent.completed = True
    session.commit()
    return 'done'


@rents.route('/rent/<rentID>/createTransaction')
@login_required
@rent_editable
def createRentTransaction(rentID):
    return render_template('createTransaction.html', rentID=rentID)


@rents.route('/rent/checkout', methods=['POST'])
@login_required
def rentCheckout():
    rent = Rent.query.filter_by(id=int(request.form['rentID'])).first_or_404()

    nonceFromTheClient = request.form['payment_method_nonce']
    print(nonceFromTheClient)

    # Create the BrainTree Transaction
    result = braintree.Transaction.sale({
        'amount': str(rent.amount),
        'payment_method_nonce': nonceFromTheClient,
        'options': {
            "submit_for_settlement": True
        }
    })
    print(result)
    return result
