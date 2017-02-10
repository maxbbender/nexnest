from flask import Blueprint, redirect, url_for, flash, render_template

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.models.listing import Listing
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing
from nexnest.models.group_listing import GroupListing

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

        unAcceptedListings = session.query(GroupListing) \
            .filter_by(landlord_show=True,
                       accepted=False,
                       completed=False,
                       group_show=True) \
            .all()

        return render_template('dashboard.html',
                               landlord=landlord,
                               dateChangeForm=dateChangeForm,
                               listings=landlord.getListings())
    else:
        flash("You are not a landlord", 'warning')
        return redirect(url_for('indexs.index'))
