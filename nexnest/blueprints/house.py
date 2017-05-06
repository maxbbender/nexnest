from flask import Blueprint, request, redirect, flash, render_template, url_for, jsonify

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.forms import HouseMessageForm, MaintenanceRequestForm, MaintenanceRequestMessageForm, GroupReportForm, LandlordReportForm
from nexnest.models.house import House
from nexnest.models.house_message import HouseMessage
from nexnest.models.maintenance import Maintenance
from nexnest.models.maintenance_message import MaintenanceMessage

from nexnest.utils.flash import flash_errors

from sqlalchemy import desc

houses = Blueprint('houses', __name__, template_folder='../templates/house')


@houses.route('/house/view/<id>', methods=['GET'])
@login_required
def view(id):
    house = session.query(House) \
        .filter_by(id=id) \
        .first()

    messages = session.query(HouseMessage) \
        .filter_by(house_id=id).order_by(desc(HouseMessage.date_created)) \
        .all()

    maintenanceRequests = session.query(Maintenance) \
        .filter_by(house_id=id).order_by(desc(Maintenance.date_created))\
        .all()

    messageForm = HouseMessageForm()
    maintenanceRequestForm = MaintenanceRequestForm()

    if house is not None:

        if house.isViewableBy(current_user):

            return render_template('viewHouse.html',
                                   house=house,
                                   landlords=house.listing.landLordsAsUsers(),
                                   messages=messages,
                                   maintenanceRequests=maintenanceRequests,
                                   messageForm=messageForm,
                                   maintenanceRequestForm=maintenanceRequestForm,
                                   GroupReportForm=GroupReportForm(),
                                   LandlordReportForm=LandlordReportForm())
        else:
            flash("This house is not occupied", "warning")
    else:
        flash("House does not exist", "warning")

    return redirect(url_for('indexs.index'))


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/message', methods=['POST'])
@login_required
def messageCreate():
    form = HouseMessageForm(request.form)

    if form.validate():

        # Group Listing
        house = session.query(House).filter_by(id=form.houseID.data).first()

        if house is not None:

            if house.isViewableBy(current_user):
                newHM = HouseMessage(house=house,
                                     content=form.content.data,
                                     user=current_user)
                session.add(newHM)
                session.commit()

                newHM.genNotifications()

        else:
            flash("Invalid Request", 'warning')
    else:
        flash_errors(form)

    return form.redirect()


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest', methods=['POST'])
@login_required
def maintenanceRequestCreate():
    form = MaintenanceRequestForm(request.form)

    if form.validate():
        house = session.query(House).filter_by(id=form.houseID.data).first()

        if house is not None:

            if current_user in house.tenants:
                newMR = Maintenance(request_type=form.requestType.data,
                                    details=form.details.data,
                                    house=house,
                                    user=current_user)
                session.add(newMR)
                session.commit()

                newMR.genNotifications()

                flash("Maintenance Request Created", 'success')
                return redirect(url_for('houses.maintenanceRequestView', id=newMR.id))
            else:
                flash("You are not a part of this house", 'warning')

        else:
            flash('Invalid Request', 'warning')
    else:
        flash_errors(form)

    form.redirect()


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest/message', methods=['POST'])
@login_required
def maintenanceRequestMessage():
    form = MaintenanceRequestMessageForm(request.form)

    if form.validate():
        maintenance = session.query(Maintenance).filter_by(id=form.maintenanceID.data).first()

        if maintenance is not None:
            if maintenance.house.isViewableBy(current_user):
                newMRMsg = MaintenanceMessage(maintenance=maintenance,
                                              content=form.content.data,
                                              user=current_user)
                session.add(newMRMsg)
                session.commit()

                newMRMsg.genNotifications()
                # RETURN BACKTO MAINTENNANCE VIEW
                return redirect(url_for('houses.maintenanceRequestView', id=maintenance.id))

        else:
            flash("Invalid Request", 'warning')

    return form.redirect()


@houses.route('/house/maintenanceRequest/<id>/view', methods=['GET'])
@login_required
def maintenanceRequestView(id):
    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.house.isViewableBy(current_user):
            # Message Form
            messageForm = MaintenanceRequestMessageForm()
            messageForm.maintenanceID = id

            # House
            house = session.query(House) \
                .filter_by(id=maintenanceRequest.house.id) \
                .first()

            # Messages
            messages = session.query(MaintenanceMessage). \
                filter_by(maintenance_id=id). \
                order_by(desc(MaintenanceMessage.date_created)).all()

            return render_template('maintenanceView.html',
                                   maintenanceRequest=maintenanceRequest,
                                   house=house,
                                   landlords=house.listing.landLordsAsUsers(),
                                   messageForm=messageForm,
                                   messages=messages)


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest/<id>/inProgress', methods=['GET'])
@login_required
def maintenanceRequestInProgress(id):
    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = 'inprogress'
            session.commit()

            maintenanceRequest.genInProgressNotifications()
    else:
        flash('Invalid Request', 'warning')

    return redirect(url_for('houses.maintenanceRequestView', id=id))


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest/<id>/completed', methods=['GET'])
@login_required
def maintenanceRequestCompleted(id):
    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = 'completed'
            session.commit()

            maintenanceRequest.genCompletedNotifications()
    else:
        flash('Invalid Request', 'warning')

    return redirect(url_for('houses.maintenanceRequestView', id=id))


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest/<id>/inProgress/ajax', methods=['GET'])
@login_required
def maintenanceRequestInProgressAJAX(id):
    errorMessage = None

    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = 'inprogress'
            session.commit()

            maintenanceRequest.genInProgressNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest/<id>/undoInProgress/ajax/<target>', methods=['GET'])
@login_required
def maintenanceRequestUndoInProgressAJAX(id, target):
    errorMessage = None

    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = target
            session.commit()

            maintenanceRequest.removeInProgressNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest/<id>/completed/ajax', methods=['GET'])
@login_required
def maintenanceRequestCompletedAJAX(id):
    errorMessage = None

    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = 'completed'
            session.commit()

            maintenanceRequest.genCompletedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})


# NOTIFICATIONS IMPLEMENTED
@houses.route('/house/maintenanceRequest/<id>/undoCompleted/ajax/<target>', methods=['GET'])
@login_required
def maintenanceRequestUndoCompletedAJAX(id, target):
    errorMessage = None

    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = target
            session.commit()

            maintenanceRequest.removeCompletedNotifications()

            return jsonify(results={'success': True})
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Reqeuest'

    return jsonify(results={'success': False, 'message': errorMessage})
