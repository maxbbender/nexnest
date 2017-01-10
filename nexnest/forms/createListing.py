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

class CreateListingForm(FlaskForm):
	street = StringField('Street Address', [Length(min=2, max=50), InputRequired()])
	city = StringField('City', [Length(min=2, max=50), InputRequired()])
	state = SelectField('State', choices=states)
	zip_code = StringField('Zipcode', [Length(min=5, max=5), InputRequired()])
	start_date = StringField('Start Date', [Length(min=5, max=15), InputRequired()])
	end_date = StringField('End Date', [Length(min=5, max=15), InputRequired()])
	unit_type = SelectField('Unit Type', choices=valid_unit_types)
	num_bedrooms = IntegerField('Number of Bedrooms', [InputRequired()])
	num_full_baths = IntegerField('Number of Full Bathrooms', [InputRequired()])
	num_half_baths = IntegerField('Number of Half Bathrooms', [InputRequired()])
	price = IntegerField('Price per Bedroom per Semester', [InputRequired()])
	square_footage = IntegerField('Square Footage of House', [InputRequired()])
	parking = SelectField('What Parking is Available', choices=valid_parking_types)
	cats = SelectField('Are Cats Allowed?', choices=yesNo)
	dogs = SelectField('Are Dogs Allowed?', choices=yesNo)
	other_pets = SelectField('Are Other Pets Allowed?', choices=yesNo)
	washer = SelectField('Is there a Washing Machine?', choices=yesNo)
	dryer = SelectField('Is there a Dryer?', choices=yesNo)
	dishwasher = SelectField('Is there a Dishwasher?', choices=yesNo)
	air_conditioning = SelectField('Is there Air Conditioning?', choices=yesNo)
	handicap = SelectField('Is the property handicap accessible?', choices=yesNo)
	furnished = SelectField('Is the property furnished?', choices=yesNo)
	utilities_included = SelectField('Are utilities included in the price?', choices=yesNo)
	emergency_maintenance = SelectField('Do you provide emergency maintenance?', choices=yesNo)
	snow_plowing  = SelectField('Do you provide snow removal?', choices=yesNo)
	garbage_service  = SelectField('Is garbage service included?', choices=yesNo)
	security_service  = SelectField('Is there a security service provided?', choices=yesNo)
	description  = TextAreaField('Please provide a detailed description of the property', [Length(min=1, max=1500), InputRequired()])
