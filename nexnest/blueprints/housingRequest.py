from flask import Blueprint, request, redirect, flash, render_template, url_for

from flask_login import login_required, current_user

housingRequests = Blueprint('housingRequests', __name__, template_folder='../templates/housingRequest')

@housingRequest.route('/houseRequest/create')
@login_required
def create():
	