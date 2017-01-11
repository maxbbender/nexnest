from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, EqualTo, Length

yesNo = [
	('0', 'No'),
	('1', 'Yes')	
]

valid_parking_types = [
	('0', 'onstreet'), 
	('1', 'offstreet'), 
	('2', 'none')
]

valid_unit_types = [
	('0', 'room'), 
	('1', 'house'), 
	('2', 'complex'),
	('3', 'apartment')
]

valid_time_periods = [
	('0', 'Month'),
	('1', 'Semester'),
	('2', 'Year'),
	('3', 'Summer')
]

states = [
	('0', 'AL'),
	('1', 'AK'),
	('2', 'AZ'),
	('3', 'AR'),
	('4', 'CA'),
	('5', 'CO'),
	('6', 'CT'),
	('7', 'DE'),
	('8', 'FL'),
	('9', 'GA'),
	('10', 'HI'),
	('11', 'ID'),
	('12', 'IL'),
	('13', 'IN'),
	('14', 'IA'),
	('15', 'KS'),
	('16', 'KY'),
	('17', 'LA'),
	('18', 'ME'),
	('19', 'MD'),
	('20', 'MA'),
	('21', 'MI'),
	('22', 'MN'),
	('23', 'MS'),
	('24', 'MO'),
	('25', 'MT'),
	('26', 'NE'),
	('27', 'NV'),
	('28', 'NH'),
	('29', 'NJ'),
	('30', 'NM'),
	('31', 'NY'),
	('32', 'NC'),
	('33', 'ND'),
	('34', 'OH'),
	('35', 'OK'),
	('36', 'OR'),
	('37', 'PA'),
	('38', 'RI'),
	('39', 'SC'),
	('40', 'SD'),
	('41', 'TN'),
	('42', 'TX'),
	('43', 'UT'),
	('44', 'VT'),
	('45', 'VA'),
	('46', 'WA'),
	('47', 'WV'),
	('48', 'WI'),
	('49', 'WY')
]

class ListingForm(FlaskForm):
	street = StringField('Street Address', [Length(min=2, max=50), InputRequired()])
	apartment_number = IntegerField('Apartment Number', [InputRequired()])
	city = StringField('City', [Length(min=2, max=50), InputRequired()])
	state = SelectField('State', choices=states)
	zip_code = StringField('Zipcode', [Length(min=5, max=5), InputRequired()])
	start_date = StringField('Start Date', [Length(min=5, max=15), InputRequired()])
	end_date = StringField('End Date', [Length(min=5, max=15), InputRequired()])
	time_period = SelectField('Length of Lease', choices=valid_time_periods)
	unit_type = SelectField('Unit Type', choices=valid_unit_types)
	num_bedrooms = IntegerField('Number of Bedrooms', [InputRequired()])
	num_full_baths = IntegerField('Number of Full Bathrooms', [InputRequired()])
	num_half_baths = IntegerField('Number of Half Bathrooms', [InputRequired()])
	price = IntegerField('Price per Bedroom per Semester', [InputRequired()])
	square_footage = IntegerField('Square Footage of House', [InputRequired()])
	parking = SelectField('What Parking is Available', choices=valid_parking_types)
	cats = BooleanField('Are Cats Allowed?')
	dogs = BooleanField('Are Dogs Allowed?')
	other_pets = BooleanField('Are Other Pets Allowed?')
	washer = BooleanField('Is there a Washing Machine?')
	dryer = BooleanField('Is there a Dryer?')
	dishwasher = BooleanField('Is there a Dishwasher?')
	air_conditioning = BooleanField('Is there Air Conditioning?')
	handicap = BooleanField('Is the property handicap accessible?')
	furnished = BooleanField('Is the property furnished?')
	utilities_included = BooleanField('Are utilities included in the price?')
	emergency_maintenance = BooleanField('Do you provide emergency maintenance?')
	snow_plowing  = BooleanField('Do you provide snow removal?')
	garbage_service  = BooleanField('Is garbage service included?')
	security_service  = BooleanField('Is there a security service provided?')
	description  = TextAreaField('Please provide a detailed description of the property', [Length(min=1, max=1500), InputRequired()])

