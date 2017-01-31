from flask import Blueprint, request, redirect, flash, render_template, url_for

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.forms import RequestListingForm

from nexnest.models.group import Group
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.listing import Listing

from nexnest.utils.flash import flash_errors
housingRequests = Blueprint('housingRequests', __name__, template_folder='../templates/housingRequest')


@housingRequests.route('/houseRequest/create', methods=['POST'])
@login_required
def create():
    form = RequestListingForm(request.form)

    if form.validate():

        # Get the Group
        group = session.query(Group) \
            .filter_by(id=form.groupID.data) \
            .first()

        if group is not None:

            if group.isEditableBy(current_user):

                # Get the listing
                listing = session.query(Listing).filter_by(id=form.listingID.data).first()

                if listing is not None:

                    # Lets create a new group listing!
                    newGL = GroupListing(group,
                                         listing,
                                         form.reqDescription.data)

                    session.add(newGL)
                    session.commit()

                    return redirect(url_for('housingRequests.view', id=newGL.id))
                else:
                    flash("Listing does not exist")
        else:
            flash("Group does not exist")
    else:
        flash_errors(form)

    return form.redirect()


@housingRequests.route('/houseRequest/view/<id>')
@login_required
def view(id):
    housingRequest = session.query(GroupListing) \
        .filter_by(id=id) \
        .first()

    messages = session.query(GroupListingMessage) \
        .filter_by(groupListingID=housingRequest.id) \
        .first()

    if housingRequest is not None:

        if current_user in housingRequest.group.getUsers():
            return render_template('housingRequestView.html',
                                   housingRequest=housingRequest,
                                   messages=messages)
        else:
            flash("You are not allowed to view this page")
    else:
        flash("Housing Request does not exist")

    return redirect(url_for('indexs.index'))
