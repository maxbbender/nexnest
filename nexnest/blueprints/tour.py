from flask import Blueprint

from flask_login import current_user, login_required

from nexnest.forms.tourForm import TourForm

tours = Blueprint('tours', __name__, template_folder='../templates/tour')


@tours.route('/tour/create')
@login_required
def createTour():
	tourForm = TourForm(request.form)

	if request.method == 'POST':

