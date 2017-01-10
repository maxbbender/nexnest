from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.loginForm import LoginForm

from nexnest.application import session

from nexnest.models.listing import Listing

from nexnest.utils.flash import flash_errors

viewListings = Blueprint('viewListings', __name__, template_folder='../templates')

@viewListings.route('/viewListing/<listingID>', methods=['GET', 'POST'])
def viewListing(listingID):
	#fake lisiting for testing
	form = LoginForm(request.form)
	viewListing = session.query(Listing).filter_by(id=listingID).first()
	return render_template('detailedListing.html', form=form, listing=viewListing, title='Listing')