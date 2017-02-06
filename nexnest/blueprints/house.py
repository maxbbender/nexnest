from flask import Blueprint, request, redirect, flash, render_template, url_for

from flask_login import login_required, current_user

from nexnest.application import session

from nexnest.forms import GroupListingMessageForm
from nexnest.models.group import Group
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.listing import Listing

from nexnest.utils.flash import flash_errors
houses = Blueprint('houses', __name__, template_folder='../templates/house')

@houses.route('/house/view/<id>', methods=['GET'])
@login_required
def view(id):
	house = session.query(GroupListing) \
		.filter_by(id=id) \
		.first()

	messages = session.query(GroupListingMessage) \
		.filter_by(groupListingID=house.id) \
		.first()

	messageForm = GroupListingMessageForm()

	if house is not None:

		if house.completed == True:

			if house.isViewableBy(current_user):
				return render_template('viewHouse.html',
									   house=house,
									   messages=messages,
									   messageForm=messageForm)
		else:
			flash("This house is not occupied", "warning")
	else:
		flash("House does not exist", "warning")

	return redirect(url_for('indexs.index'))

