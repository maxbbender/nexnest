from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from flask_login import current_user

from nexnest.application import session

from nexnest.models.group_user import GroupUser
from nexnest.models.group import Group

from nexnest.utils.flash import flash_errors

viewGroups = Blueprint('viewGroups', __name__, template_folder='../templates')

@viewGroups.route('/viewGroup/<groupID>', methods=['GET', 'POST'])
def viewGroup(groupID):
	#fake lisiting for testing
	viewGroup = session.query(Group).filter_by(id=groupID).first()
	return render_template('group.html', group=viewGroup, title='Group')