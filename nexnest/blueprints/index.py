from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from ..forms.loginForm import LoginForm

from flask_login import login_required
from nexnest.application import session

from nexnest.models.listing import Listing

from nexnest.utils.flash import flash_errors

indexs = Blueprint('indexs', __name__, template_folder='../templates')

@indexs.route('/')
@indexs.route('/index')
def index():
	form = LoginForm(request.form)
	allListings = session.query(Listing).all()
	listings = [  # fake array of listings
	        { 
	            'Street': '25 Myrtle Lane', 
	            'City': 'Patchogue',
	            'State': 'NY',
	            'ZipCode': '11772',
	            'NumBedrooms': '3',
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
	            'security_service': 'yes'
	        },
	        { 
	            'Street': '51 Bennet Avenue', 
	            'City': 'Patchogue',
	            'State': 'NY',
	            'ZipCode': '11772',
	            'NumBedrooms': '2',
	            'Price': '1200',
	            'img':'./static/img/testHouse2.jpg',
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
	            'security_service': 'yes' 
	        },
	        { 
	            'Street': '15 Potter Street', 
	            'City': 'Patchogue',
	            'State': 'NY',
	            'ZipCode': '11772',
	            'NumBedrooms': '3',
	            'Price': '1800',
	            'img':'./static/img/testHouse3.jpg',
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
	            'security_service': 'yes' 
	        },
	        { 
	            'Street': '114 Jennings Avenue', 
	            'City': 'Patchogue',
	            'State': 'NY',
	            'ZipCode': '11772',
	            'NumBedrooms': '3',
	            'Price': '2000',
	            'img':'./static/img/testHouse4.jpg',
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
	            'security_service': 'yes'
	        },
	        { 
	            'Street': '7 Bay Avenue', 
	            'City': 'Patchogue',
	            'State': 'NY',
	            'ZipCode': '11772',
	            'NumBedrooms': '5',
	            'Price': '1800',
	            'img':'./static/img/testHouse5.jpg',
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
	            'security_service': 'yes'
	        },
	        { 
	            'Street': '14 Maple Steet', 
	            'City': 'Patchogue',
	            'State': 'NY',
	            'ZipCode': '11772',
	            'NumBedrooms': '2',
	            'Price': '500',
	            'img':'./static/img/testHouse6.jpg',
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
	            'security_service': 'yes'
	        },
		]
	if request.method == 'POST' and form.validate():
		#user = User(form.username.data, form.email.data,
		#            form.password.data)
		#db_session.add(user)
		flash('Login Successfull')
		return redirect(url_for('indexs.index'))
	return render_template('index.html', 
							form=form,
							listings = allListings,
							title='NexNest')
@indexs.route('/test')
@login_required
def test():
    return render_template('test.html')
