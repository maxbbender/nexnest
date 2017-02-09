from flask import Blueprint, request, redirect, flash, render_template, url_for

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.forms import HouseMessageForm, MaintenanceRequestForm
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


@houses.route('/house/maintenanceRequest/request')
@login_required
def maintenanceRequestCreate():
    form = MaintenanceRequestForm(request.form)

    if form.validate():
        house = session.query(House).filter_by(id=form.houseID.data).first()

        if house is not None:

            if current_user in house.tenants:
                newMR = Maintenance(request_type=form.requestType.data,
                                    details=form.details.data, house=house)
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


            
            
