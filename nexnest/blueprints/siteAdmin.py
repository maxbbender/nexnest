
from flask import (Blueprint, abort, flash, jsonify, render_template, request,
                   url_for, redirect)
from flask_login import current_user, login_required

from nexnest import db
from nexnest.forms import CreateCouponForm, ContactForm
from nexnest.models.coupon import Coupon
from nexnest.models.user import User
from nexnest.utils.coupon import couponExists
from nexnest.utils.misc import idGenerator
from nexnest.utils.email import send_email
from nexnest.utils.flash import flash_errors

siteAdmin = Blueprint('siteAdmin', __name__,
                      template_folder='../templates/siteAdmin')

session = db.session


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

                flash('Coupon Created!', 'success')

            else:
                newCoupon = Coupon(percentage_off=form.percentageOff.data,
                                   coupon_key=form.couponKey.data,
                                   unlimited=False,
                                   uses=form.uses.data)
                session.add(newCoupon)
                session.commit()

                flash('Coupon Created!', 'success')
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

        keyCount = session.query(Coupon).filter_by(
            coupon_key=newRandomKey).count()

    return jsonify({'couponKey': newRandomKey})


@siteAdmin.route('/allCoupons', methods=['GET'])
@login_required
def allCoupons():
    coupons = Coupon.query.all()

    return render_template('/allCoupons.html',
                           coupons=coupons)


@siteAdmin.route('/coupon/<couponID>/updateUses/<numUses>')
@login_required
def updateCouponUses(couponID, numUses):
    coupon = Coupon.query.filter_by(id=couponID).first_or_404()

    coupon.uses = numUses
    session.commit()

    return redirect(url_for('siteAdmin.siteAdminDashboard'))


@siteAdmin.route('/coupon/<couponID>/delete')
@login_required
def deleteCoupon(couponID):
    coupon = Coupon.query.filter_by(id=couponID).first()

    if coupon is None:
        if request.is_xhr:
            return jsonify({'success': False, 'message': "Coupon doesn\'t exist"})
        else:
            flash("Coupon doesn't exist", 'danger')
    else:
        session.delete(coupon)
        session.commit()
        if request.is_xhr:
            return jsonify({'success': True})
        else:
            flash('Coupon Deleted', 'success')

    return redirect(url_for('siteAdmin.siteAdminDashboard'))


@siteAdmin.route('/searchUsers/lastName/<lastName>')
@login_required
def searchUsersByLastName(lastName):
    allUsers = User.query.filter(User.lname.ilike(lastName + "%")).all()

    userReturnArray = []

    for user in allUsers:
        userReturnArray.append(user.serialize)

    return jsonify({'users': userReturnArray})


@siteAdmin.route('/contactUs', methods=['POST'])
@login_required
def contactUs():
    form = ContactForm()

    if form.validate():
        user = current_user
        htmlResponse = '''
            <h1>NEW CONTACT FORM AHHHHHHHHHHHHHHHHHHHHHHHHH</h1>
            From %r<br>
            Full Name Proivded: %s<br>
            Phone Number: %s<br>
            Message: %s<br>
            ''' % (user, form.name.data, form.phone.data, form.message.data)

        send_email(subject='Contact Us Form',
                   sender='no_reply@nexnest.com',
                   recipients=['contact@nexnest.com'],
                   html_body=htmlResponse)
        flash('Thank you for contacting Nexnest, we will address your issue and get back to you as soon as possible', 'success')
    else:
        flash_errors(form)

    return form.redirect()
