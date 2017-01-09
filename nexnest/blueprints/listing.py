from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.loginForm import LoginForm
# from nexnest.application import session

listings = Blueprint('listings', __name__, template_folder='../templates')

@listings.route('/listing', methods=['GET', 'POST'])
def listing():
	#fake lisiting for testing
	form = LoginForm(request.form)
	listing = { 
	            'Street': '25 Myrtle Lane', 
	            'City': 'Patchogue',
	            'State': 'NY',
	            'ZipCode': '11772',
	            'NumBedrooms': '3',
	            'num_full_baths': '2',
	            'num_half_baths': '1',
	            'Price': '2000',
	            'img': './static/img/testHouse.jpg',
	            'start_date': '06/01/17',
	            'end_date': '05/31/17',
	            'unit_type': 'House',
	            'square_footage': '1500',
	            'parking': '3 car driveway',
	            'cats': 'no',
	            'dogs': 'yes',
	            'other_pets': 'we can discuss',
	            'washer': 'yes',
	            'dryer': 'yes',
	            'dishwasher': 'yes',
	            'air_conditioning': 'yes',
	            'handicap': 'no',
	            'furnished': 'no',
	            'utilities_included': 'no',
	            'emergency_maintenance': 'yes',
	            'snow_plowing': 'yes',
	            'garbage_service': 'yes',
	            'security_service': 'yes',
	            'description': 'Lovely 2 story house in a nice neighborhood. Kitchen, backroom, living room, office, family room, bathroom and multiple closets on first floor.',
	            'demoImg1': './static/img/testLivingRoom.jpg',
	            'demoImg2': './static/img/testKitchen.jpg',
	            'demoImg3': './static/img/testBedroom.jpg',
	            'demoImg4': './static/img/testBathroom.jpg'
	}
	return render_template('detailedListing.html', form=form, listing=listing, title='Listing')