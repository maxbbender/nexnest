from flask import Blueprint, redirect, url_for, flash, render_template

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.models.listing import Listing
from nexnest.models.landlord import Landlord
from nexnest.models.landlord_listing import LandlordListing

landlords = Blueprint('landlords',
                      __name__,
                      template_folder='../templates/landlord')


@landlords.route('/landlord/dashboard')
@login_required
def landlordDashboard():
    if current_user.isLandlord:
        landlord = session.query(Landlord) \
            .filter_by(user_id=current_user.id) \
            .first()

        return render_template('dashboard.html',
                               landlord=landlord,
                               listings=landlord.getListings())
    else:
        flash("You are not a landlord", 'warning')
        return redirect(url_for('indexs.index'))
