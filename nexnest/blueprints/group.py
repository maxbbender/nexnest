from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..forms.createGroup import CreateGroupForm

from nexnest.application import session

from nexnest.models.group import Group

from nexnest.utils.flash import flash_errors

groups = Blueprint('groups', __name__, template_folder='../templates')

@groups.route('/createGroup', methods=['GET', 'POST'])
def createGroup():
    form = CreateGroupForm(request.form)
    if request.method == 'POST' and form.validate():
        newGroup = Group(name=form.name.data,
                        leader=current_user)
        session.add(newGroup)
        session.commit()
        flash('Group Created')
        return redirect(url_for('indexs.index', groupID=newGroup.id))
    return render_template('createGroup.html', form=form, title='Create Group')

#@groups.route('/myGroup', methods=['GET', 'POST'])
#def viewGroup(groupID):
	#currentUser.myGroup
#	return render_template('group.html', group=viewGroup, title='Group')