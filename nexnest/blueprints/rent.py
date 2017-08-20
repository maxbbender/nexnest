from flask import Blueprint, render_template, request, jsonify

from flask_login import login_required
import braintree

from nexnest.decorators import rent_editable, rent_viewable
from nexnest.models.rent import Rent

from nexnest import db

session = db.session


rents = Blueprint('rents', __name__, template_folder='../templates/rents')


@rents.route('/rent/<rentID>/completed')
@login_required
@rent_editable
def markCompleted(rentID):
    rent = Rent.query.filter_by(id=rentID).first_or_404()

    if not rent.completed:
        rent.completed = True
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Rent has already been marked as completed!'})


@rents.route('/rent/<rentID>/unCompleted')
@login_required
@rent_editable
def markUnCompleted(rentID):
    rent = Rent.query.filter_by(id=rentID).first_or_404()

    if rent.completed:
        rent.completed = False
        session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Rent is already marked as uncomplete!'})


# @rents.route('/rent/<rentID>/createTransaction')
# @login_required
# @rent_editable
# def createRentTransaction(rentID):
#     return render_template('createTransaction.html', rentID=rentID)


# @rents.route('/rent/checkout', methods=['POST'])
# @login_required
# def rentCheckout():
#     rent = Rent.query.filter_by(id=int(request.form['rentID'])).first_or_404()

#     nonceFromTheClient = request.form['payment_method_nonce']
#     print(nonceFromTheClient)

#     # Create the BrainTree Transaction
#     result = braintree.Transaction.sale({
#         'amount': str(rent.amount),
#         'payment_method_nonce': nonceFromTheClient,
#         'options': {
#             "submit_for_settlement": True
#         }
#     })
#     print(result)
#     return result
