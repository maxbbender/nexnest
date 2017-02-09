from flask import Blueprint, request, redirect, flash, render_template, url_for

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.forms import HouseMessageForm, MaintenanceRequestForm, MaintenanceRequestMessageForm
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.house import House
from nexnest.models.house_message import HouseMessage
from nexnest.models.maintenance import Maintenance
from nexnest.models.maintenance_message import MaintenanceMessage

from nexnest.utils.flash import flash_errors

from sqlalchemy import asc, desc

houses = Blueprint('houses', __name__, template_folder='../templates/house')


@houses.route('/house/view/<id>', methods=['GET'])
@login_required
def view(id):
    house = session.query(House) \
        .filter_by(id=id) \
        .first()

    messages = session.query(HouseMessage) \
        .filter_by(id=id).order_by(desc(GroupListingMessage.date_created)) \
        .all()

    messageForm = HouseMessageForm()

    if house is not None:

        if house.isViewableBy(current_user):

            if house.completed:
                return render_template('viewHouse.html',
                                       house=house,
                                       landlords=house.listing.landLordsAsUsers(),
                                       messages=messages,
                                       messageForm=messageForm)
        else:
            flash("This house is not occupied", "warning")
    else:
        flash("House does not exist", "warning")

    return redirect(url_for('indexs.index'))


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

        else:
            ("Invalid Request", 'warning')
    else:
        flash_errors(form)

    return form.redirect()


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
                                    house=house)
                session.add(newMR)
                session.commit()

                flash("Maintenance Request Created", 'success')
                return redirect(url_for('houses.view', id=house.id))
            else:
                flash("You are not a part of this house", 'warning')

        else:
            flash('Invalid Request', 'warning')
    else:
        flash_errors(form)

    form.redirect()


@houses.route('/house/maintenanceRequest/<id>/message', methods=['POST'])
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

        else:
            flash("Invalid Request", 'warning')


@houses.route('/house/maintenanceRequest/<id>/view', methods=['GET'])
@login_required
def maintenanceRequestView(id):
    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.group.isViewableBy(current_user):
            # Message Form
            messageForm = MaintenanceRequestMessageForm()
            messageForm.maintenanceID = id

            # Messages
            messages = session.query(MaintenanceMessage). \
                filter_by(maintenance_id=id). \
                order_by(desc(MaintenanceMessage.date_created)).all()

            return render_template('maintenanceView.html',
                                   maintenanceRequest=maintenanceRequest,
                                   messageForm=messageForm,
                                   message=messages)


@houses.route('/house/maintenanceRequest/<id>/inProgress', methods=['GET'])
@login_required
def maintenanceRequestInProgress(id):
    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = 'inprogress'
            session.commit()
    else:
        flash('Invalid Request', 'warning')

    return redirect(url_for('houses.maintenanceRequestView', id=id))


@houses.route('/house/maintenanceRequest/<id>/completed', methods=['GET'])
@login_required
def maintenanceRequestCompleted(id):
    maintenanceRequest = session.query(Maintenance).filter_by(id=id).first()

    if maintenanceRequest is not None:
        if maintenanceRequest.isEditableBy(current_user):
            maintenanceRequest.status = 'completed'
            session.commit()
    else:
        flash('Invalid Request', 'warning')

    return redirect(url_for('houses.maintenanceRequestView', id=id))
