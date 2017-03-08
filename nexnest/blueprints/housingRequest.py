from flask import Blueprint, request, redirect, flash, render_template, url_for, jsonify

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.forms import GroupListingForm, GroupListingMessageForm, LeaseUploadForm
from nexnest.models.group import Group
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.listing import Listing
from nexnest.models.house import House
from nexnest.models.security_deposit import SecurityDeposit

from nexnest.utils.flash import flash_errors
from nexnest.utils.file import isPDF

from werkzeug.utils import secure_filename

from sqlalchemy import desc

import os

housingRequests = Blueprint(
    'housingRequests', __name__, template_folder='../templates/housingRequest')


@housingRequests.route('/houseRequest/create', methods=['POST'])
@login_required
def create():
    form = GroupListingForm(request.form)

    if form.validate():

        # Get the Group
        group = session.query(Group) \
            .filter_by(id=form.groupID.data) \
            .first()

        if group is not None:

            if group.isEditableBy(current_user):

                # Get the listing
                listing = session.query(Listing).filter_by(
                    id=form.listingID.data).first()

                if listing is not None:

                    # Lets create a new group listing!
                    newGL = GroupListing(group,
                                         listing)

                    session.add(newGL)
                    session.commit()

                    newGLM = GroupListingMessage(groupListing=newGL,
                                                 content=form.reqDescription.data,
                                                 user=current_user)

                    session.add(newGLM)
                    session.commit()

                    return redirect(url_for('housingRequests.view', id=newGL.id))
                else:
                    flash("Listing does not exist")
        else:
            flash("Group does not exist")
    else:
        flash_errors(form)

    return form.redirect()


@housingRequests.route('/houseRequest/view/<id>', methods=['GET'])
@login_required
def view(id):
    housingRequest = session.query(GroupListing) \
        .filter_by(id=id) \
        .first()

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
                                   hasLease=housingRequest.hasLease())
    else:
        flash("Housing Request does not exist", "warning")

    return redirect(url_for('indexs.index'))


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

        else:
            flash("House Request does not exist", 'info')
    else:
        flash_errors(form)

    return form.redirect()


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

            flash("Group Accepted", 'success')
            return redirect(url_for('housingRequests.view', id=groupListing.id))
    else:
        flash("Invalid Request", 'warning')
        return redirect(url_for('indexs.index'))


@housingRequests.route('/houseRequest/<id>/deny', methods=['GET'])
@login_required
def denyRequest(id):
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            groupListing.landlord_show = False
            session.commit()

            flash('Request Denied', 'success')
            return redirect(url_for('landlords.landlordDashboard'))

    else:
        flash("Invalid Request", 'warning')
        return redirect(url_for('indexs.index'))


@housingRequests.route('/houseRequest/<id>/confirm', methods=['GET'])
@login_required
def confirmRequest(id):
    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:

        if groupListing.isEditableBy(current_user):
            groupListing.completed = True
            session.commit()

            flash('House Confirmed ~ Congrats!', 'success')

            # Create the House Object
            house = House(listing=groupListing.listing,
                          group=groupListing.group)

            session.add(house)
            session.commit()

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


@housingRequests.route('/houseRequest/<id>/accept/ajax', methods=['GET'])
@login_required
def acceptHousingRequestAJAX(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user):
            groupListing.accepted = True
            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


@housingRequests.route('/houseRequest/<id>/undoAccept/ajax', methods=['GET'])
@login_required
def acceptHousingRequestAJAXUndo(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user):
            groupListing.accepted = False
            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


@housingRequests.route('/houseRequest/<id>/complete/ajax', methods=['GET'])
@login_required
def completeHousingRequestAJAX(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user):
            groupListing.completed = True
            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


@housingRequests.route('/houseRequest/<id>/undoComplete/ajax', methods=['GET'])
@login_required
def completeHousingRequestAJAXUndo(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user):
            groupListing.completed = False
            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


@housingRequests.route('/houseRequest/<id>/deny/ajax', methods=['GET'])
@login_required
def denyHousingRequestAJAX(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user):
            groupListing.group_show = False
            groupListing.landlord_show = False
            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


@housingRequests.route('/houseRequest/<id>/undoDeny/ajax', methods=['GET'])
@login_required
def denyHousingRequestAJAXUndo(id):
    errorMessage = None

    groupListing = session.query(GroupListing).filter_by(id=id).first()

    if groupListing is not None:
        if groupListing.isEditableBy(current_user):
            groupListing.group_show = True
            groupListing.landlord_show = True
            session.commit()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})
