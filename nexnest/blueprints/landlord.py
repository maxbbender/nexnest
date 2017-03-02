from flask import Blueprint, redirect, url_for, flash, render_template

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.models.landlord import Landlord

from nexnest.forms import TourDateChangeForm

landlords = Blueprint('landlords',
                      __name__,
                      template_folder='../templates/landlord')


@landlords.route('/landlord/dashboard')
@login_required
def landlordDashboard():
    dateChangeForm = TourDateChangeForm()
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        unAcceptedHousingRequests, acceptedHousingRequests, completedHousingRequests = landlord.getHousingRequests()
        openMaintenanceRequests, inProgressMaintenanceRequests, completedMaintenanceRequests = landlord.getMaintenanceRequests()

        requestedTours, scheduledTours = landlord.getActiveTours()

        return render_template('dashboard.html',
                               landlord=landlord,
                               dateChangeForm=dateChangeForm,
                               listings=landlord.getListings(),
                               requestedTours=requestedTours,
                               scheduledTours=scheduledTours,
                               unAcceptedHousingRequests=unAcceptedHousingRequests,
                               acceptedHousingRequests=acceptedHousingRequests,
                               completedHousingRequests=completedHousingRequests,
                               houses=landlord.getHouses(),
                               openMaintenanceRequests=openMaintenanceRequests,
                               inProgressMaintenanceRequests=inProgressMaintenanceRequests,
                               completedMaintenanceRequests=completedMaintenanceRequests)
    else:
        flash("You are not a landlord", 'warning')
        return redirect(url_for('indexs.index'))
