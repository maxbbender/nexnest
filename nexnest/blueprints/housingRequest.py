from flask import Blueprint, request, redirect, flash, render_template, url_for, jsonify

from flask_login import login_required, current_user

from nexnest.forms import GroupListingForm, GroupListingMessageForm, LeaseUploadForm, GroupReportForm, LandlordReportForm
from nexnest.models.group import Group
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.listing import Listing
from nexnest.models.house import House
from nexnest.models.security_deposit import SecurityDeposit

from nexnest.utils.flash import flash_errors
from nexnest.utils.file import isPDF
from nexnest.utils.house import createHouse

from werkzeug.utils import secure_filename

from sqlalchemy import desc

import os

from flask import current_app as app
from nexnest import db

session = db.session


housingRequests = Blueprint(
    'housingRequests', __name__, template_folder='../templates/housingRequest')


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/create', methods=['POST'])
@login_required
def create():
    rLForm = GroupListingForm(request.form)
    if rLForm.validate():
        group = session.query(Group) \
            .filter_by(id=rLForm.groupID.data) \
            .first()

        if group is not None:

            # Can the current user take actions on the group?
            if group.isEditableBy(current_user):
                listing = session.query(Listing) \
                    .filter_by(id=rLForm.listingID.data) \
                    .first()

                # Make sure there isn't already a request
                glCheck = GroupListing.query.filter_by(group=group, listing=listing).count()

                if listing is not None:

                    if glCheck == 0:

                        newGL = GroupListing(group=group,
                                             listing=listing)
                        session.add(newGL)
                        session.commit()

                        newGL.genNotifications()

                        if rLForm.reqDescription.data != "":

                            newGLM = GroupListingMessage(groupListing=newGL,
                                                         user=current_user,
                                                         content=rLForm.reqDescription.data)

                            session.add(newGLM)
                            session.commit()

                        flash("You have requested to live at this listing!", 'success')

                        # Invalidate all open group invitations
                        newGL.group.invalidateOpenInvitations()

                        return redirect(url_for('housingRequests.view', id=newGL.id))
                    else:
                        flash('%s has already requested to live at %s!' % (group.name, listing.briefStreet), 'danger')
                else:
                    flash("Listing does not exist", 'warning')

        else:
            flash("Group does not exist", 'warning')

    else:
        flash_errors(rLForm)

    return rLForm.redirect()


@housingRequests.route('/houseRequest/view/<id>', methods=['GET'])
@login_required
def view(id):
    housingRequest = session.query(GroupListing) \
        .filter_by(id=id) \
        .first()

    if housingRequest.completed:
        house = session.query(House).filter_by(listing_id=housingRequest.listing_id).first()

        return redirect(url_for('houses.view', id=house.id))

    messages = session.query(GroupListingMessage) \
        .filter_by(groupListingID=housingRequest.id).order_by(desc(GroupListingMessage.date_created)) \
        .all()

    messageForm = GroupListingMessageForm()
    leaseUploadForm = LeaseUploadForm()

    leaseUploadForm.groupListingID.data = id

    if housingRequest is not None:

        if housingRequest.isViewableBy(current_user):
            return render_template('housingRequestView.html',
                                   housingRequest=housingRequest,
                                   landlords=housingRequest.listing.landLordsAsUsers(),
                                   messages=messages,
                                   messageForm=messageForm,
                                   leaseUploadForm=leaseUploadForm,
                                   hasLease=housingRequest.hasLease(),
                                   GroupReportForm=GroupReportForm(),
                                   LandlordReportForm=LandlordReportForm())
    else:
        flash("Housing Request does not exist", "warning")

    return redirect(url_for('indexs.index'))


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/message', methods=['POST'])
@login_required
def messageCreate():
    form = GroupListingMessageForm(request.form)

    if form.validate():

        # Group Listing
        gl = session.query(GroupListing).filter_by(
            id=form.groupListingID.data).first()

        if gl is not None:

            if gl.isViewableBy(current_user):
                newGLM = GroupListingMessage(groupListing=gl,
                                             content=form.content.data,
                                             user=current_user)
                session.add(newGLM)
                session.commit()

                newGLM.genNotifications()

        else:
            flash("House Request does not exist", 'info')
    else:
        flash_errors(form)

    return form.redirect()


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/accept', methods=['GET'])
@login_required
def acceptRequest(id):
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            # At this point the house request is accepted and security deposits
            # must be paid.
            groupListing.accepted = True
            groupListing.group.invalidateOpenInvitations()
            session.commit()

            # Create Security Deposit records
            for user in groupListing.group.acceptedUsers:
                newSecurityDeposit = SecurityDeposit(user=user,
                                                     groupListing=groupListing)

                session.add(newSecurityDeposit)
                session.commit()

            groupListing.genAcceptedNotifications()

            flash("Group Accepted", 'success')
            return redirect(url_for('housingRequests.view', id=groupListing.id))
    else:
        flash("Invalid Request", 'warning')
        return redirect(url_for('indexs.index'))


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/deny', methods=['GET'])
@login_required
def denyRequest(id):
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            groupListing.landlord_show = False
            groupListing.group_show = False
            session.commit()

            groupListing.genDeniedNotifications()

            flash('Request Denied', 'success')
            return redirect(url_for('landlords.landlordDashboard'))

    else:
        flash("Invalid Request", 'warning')
        return redirect(url_for('indexs.index'))


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/confirm', methods=['GET'])
@login_required
def confirmRequest(id):
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            groupListing.completed = True
            groupListing.listing.show = False
            session.commit()

            flash('Your House Request for %s has been completed! Welcome to your new house!' % groupListing.listing.street, 'success')

            house = createHouse(groupListing.listing, groupListing.group)

            groupListing.genCompletedNotifications()

            return redirect(url_for('houses.view', id=house.id))
    else:
        flash("Invalid Request", 'warning')
        return redirect(url_for('indexs.index'))


@housingRequests.route('/houseRequest/<id>/securityDeposit/<userID>/paid')
@login_required
def paySecurityDeposit(id, userID):
    groupListing = session.query(GroupListing) \
        .filter_by(id=id) \
        .first()
    errorMessage = None
    if groupListing is not None:
        if groupListing.isEditableBy(user=current_user, toFlash=False):
            securityDeposit = session.query(SecurityDeposit) \
                .filter_by(group_listing_id=groupListing.id, user_id=userID) \
                .first()

            if securityDeposit is not None:
                if not securityDeposit.completed:
                    securityDeposit.completed = True
                    session.commit()
                    return jsonify(results={'success': True})
                else:
                    errorMessage = "Security Deposit already paid"
            else:
                errorMessage = "Invalid Reqeust"
    else:
        errorMessage = "Invalid Request"

    return jsonify(results={'success': False, 'message': errorMessage})


@housingRequests.route('/houseRequest/<id>/securityDeposit/<userID>/unPaid')
@login_required
def unPaySecurityDeposit(id, userID):
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            securityDeposit = session.query(SecurityDeposit).filter_by(
                group_listing_id=groupListing.id, user_id=userID).first()

            if securityDeposit is not None:
                if securityDeposit.completed:
                    securityDeposit.completed = False
                    session.commit()
                    return jsonify(results={'success': True})

                else:
                    errorMessage = "Security Deposit already paid"
            else:
                errorMessage = "Invalid Reqeust"
    else:
        errorMessage = "Invalid Request"

    return jsonify(results={'success': False, 'message': errorMessage})


@housingRequests.route('/houseRequest/<id>/securityDeposit/allPaid', methods=['GET'])
@login_required
def allSecurityDepositPaid(id):
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            allSecurityDeposits = session.query(SecurityDeposit).filter_by(
                group_listing_id=groupListing.id).all()
            for securityDeposit in allSecurityDeposits:
                securityDeposit.completed = True
            session.commit()
    else:
        flash("Invalid Request", 'warning')

    return redirect(url_for('housingRequests.view', id=groupListing.id))


@housingRequests.route('/houseRequest/leaseUpload', methods=['POST'])
@login_required
def uploadLease():
    form = LeaseUploadForm(request.form)

    if form.validate():
        groupListing = session.query(GroupListing).filter_by(
            id=form.groupListingID.data).first()

        if groupListing is not None:
            if groupListing.isEditableBy(current_user):
                if groupListing.canChangeLease():

                    newLease = request.files['lease']

                    if newLease.filename == '':
                        flash("No selected file", 'warning')
                        return form.redirect()

                    filename = secure_filename(newLease.filename)

                    if newLease and isPDF(filename):
                        # We are going to save the lease as groupListingLease4
                        # if the groupListing is 4

                        fileSavePath = './nexnest/uploads/leases/groupListingLease%d.pdf' % groupListing.id

                        if os.path.exists(fileSavePath):
                            flash(
                                "Lease already exists for house. Overwriting", 'info')
                            os.remove(fileSavePath)

                        flash('Lease Uploaded', 'success')
                        newLease.save(fileSavePath)
                        return redirect(url_for('housingRequests.view', id=groupListing.id))
                    else:
                        flash('Lease must be a pdf', 'warning')
        else:
            flash('Invalid Request', 'warning')
    else:
        flash_errors(form)

    return form.redirect()


@housingRequests.route('/houseRequest/<id>/allLeasesSubmitted', methods=['GET'])
@login_required
def allLeasesSubmitted():
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            groupListing.all_leases_submitted = True
            session.commit()
            return redirect(url_for('housingRequests.view', id=id))
    else:
        flash('Invalid Request', 'warning')

    return redirect(url_for('indexs.index'))


@housingRequests.route('/houseRequest/<id>/allLeasesSubmitted/ajax', methods=['GET'])
@login_required
def leasesSubmittedAJAX(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user, toFlash=False):
            if groupListing.all_leases_submitted:
                groupListing.all_leases_submitted = False
            else:
                groupListing.all_leases_submitted = True

            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/accept/ajax', methods=['GET'])
@login_required
def acceptHousingRequestAJAX(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user, toFlash=False):
            groupListing.accepted = True
            groupListing.group.invalidateOpenInvitations()
            session.commit()

            # Create Security Deposit records
            for user in groupListing.group.acceptedUsers:
                newSecurityDeposit = SecurityDeposit(user=user,
                                                     groupListing=groupListing)

                session.add(newSecurityDeposit)
                session.commit()

            groupListing.genAcceptedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/undoAccept/ajax', methods=['GET'])
@login_required
def acceptHousingRequestAJAXUndo(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user, toFlash=False):
            groupListing.accepted = False
            session.commit()

            groupListing.undoAcceptedNotifications()

            # We need to remove all the security deposit records
            session.query(SecurityDeposit).filter_by(group_listing_id=groupListing.id).delete()
            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/complete/ajax', methods=['GET'])
@login_required
def completeHousingRequestAJAX(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user, toFlash=False):
            groupListing.completed = True
            groupListing.listing.show = False
            session.commit()

            newHouse = createHouse(groupListing.listing, groupListing.group)

            if newHouse is not None:
                return jsonify(results={'success': True})
            else:
                return jsonify(results={'success': False, 'message': 'House has already been created!'})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/undoComplete/ajax', methods=['GET'])
@login_required
def completeHousingRequestAJAXUndo(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user, toFlash=False):
            groupListing.completed = False
            session.commit()

            groupListing.undoCompletedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/deny/ajax', methods=['GET'])
@login_required
def denyHousingRequestAJAX(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user, toFlash=False):
            groupListing.group_show = False
            groupListing.landlord_show = False
            session.commit()

            groupListing.genDeniedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@housingRequests.route('/houseRequest/<id>/undoDeny/ajax', methods=['GET'])
@login_required
def denyHousingRequestAJAXUndo(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user, toFlash=False):
            groupListing.group_show = True
            groupListing.landlord_show = True
            session.commit()

            groupListing.undoDeniedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})
