from flask import Blueprint, render_template, abort, jsonify, request, flash
from flask_login import login_required, current_user

from nexnest.application import session
from nexnest.forms import CreateCouponForm
from nexnest.utils.coupon import couponExists
from nexnest.utils.misc import idGenerator


from nexnest.models.coupon import Coupon
from nexnest.models.user import User


siteAdmin = Blueprint('siteAdmin', __name__, template_folder='../templates/siteAdmin')


@siteAdmin.before_request
def isSiteAdmin():
    if not current_user.is_authenticated:
        if request.is_xhr:
            return jsonify({'success': False, 'message': 'Permissions Error'})
        else:
            abort(403)

    if not current_user.isAdmin:
        if request.is_xhr:
            return jsonify({'success': False, 'message': 'Permissions Error'})
        else:
            abort(403)


@siteAdmin.route('/dashboard', methods=['GET'])
@login_required
def siteAdminDashboard():
    return render_template('siteAdminDashboard.html')


@siteAdmin.route('/createCoupon', methods=['GET', 'POST'])
@login_required
def createCoupon():
    form = CreateCouponForm()

    if form.validate_on_submit():
        if not couponExists(form.couponKey.data):
            if form.unlimited.data:
                newCoupon = Coupon(percentage_off=form.percentageOff.data,
                                   coupon_key=form.couponKey.data,
                                   unlimited=True)
                session.add(newCoupon)
                session.commit()
                flash('Cpupon Created!', 'success')

            else:
                newCoupon = Coupon(percentage_off=form.percentageOff.data,
                                   coupon_key=form.couponKey.data,
                                   unlimited=False,
                                   uses=form.uses.data)
                session.add(newCoupon)
                session.commit()
                flash('Cpupon Created!', 'success')
        else:
            flash('Coupon already exists', 'danger')
            return form.redirect()

    else:
        return render_template('createCoupon.html',
                               form=form)

    return form.redirect()


@siteAdmin.route('/getRandomCouponKey', methods=['GET'])
@login_required
def randomCouponKey():
    newRandomKey = idGenerator()

    keyCount = session.query(Coupon).filter_by(coupon_key=newRandomKey).count()

    while keyCount > 0:
        newRandomKey = idGenerator()

        keyCount = session.query(Coupon).filter_by(coupon_key=newRandomKey).count()

    return jsonify({'couponKey': newRandomKey})


@siteAdmin.route('/searchUsers/lastName/<lastName>')
@login_required
def searchUsersByLastName(lastName):
    allUsers = User.query.filter(User.lname.ilike(lastName + "%")).all()

    userReturnArray = []

    for user in allUsers:
        userReturnArray.append(user.serialize)

    return jsonify({'users': userReturnArray})


# @siteAdmin.route('/resetPassword/<userID>/')
