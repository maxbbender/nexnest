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

    if request.method == 'POST' and form.validate():  # Insert new group
        # First me must check to make sure that the current_user
        # isn't trying to create a group that conflicts with
        # other dates of groups user is a part of

        groupHasConflict = None
        conflict = False
        for group in current_user.accepted_groups:
            if form.start_date.data < group.start_date and form.end_date.data > group.start_date:
                # If I start before the group start, but end anywhere after
                # group start, this conflicts with current group
                groupHasConflict = group
                conflict = True
                break
            elif form.start_date.data >= group.start_date and form.start_date.data <= group.end_date:
                # If I start after the group starts, but not after group ends,
                # also conflict with current group
                groupHasConflict = group
                conflict = True
                break

        if not conflict:
            newGroup = Group(name=form.name.data,
                             leader=current_user,
                             start_date=form.start_date.data,
                             end_date=form.end_date.data)

            session.add(newGroup)
            session.commit()

            groupUser()
            flash('Group Created')
            return redirect(url_for('groups.viewGroup', group_id=newGroup.id))
        else:
            flash("Conflict with Group %s. Cannot create group in same time period as %s. Start(%s) End(%s)" % (
                groupHasConflict.name, groupHasConflict.name, groupHasConflict.start_date, groupHasConflict.end_date))
            return redirect(url_for('groups.createGroup'))
    else:
        return render_template('createGroup.html', form=form)


@groups.route('/viewGroup/<group_id>')
def viewGroup(group_id):
    # First lets check that the current user is apart of the group
    group = session.query(Group).filter_by(id=group_id).first()

    if group in current_user.accepted_groups:
        return render_template('group/viewGroup.html', group=group)
    else:
        flash("You are not able to view a group you are not a part of")
        return redirect(url_for('indexs.index'))


# @groups.route('/myGroups', methods=['GET', 'POST'])
# def viewGroup(groupID):
#     currentUser.myGroup
#   return render_template('group.html', group=viewGroup, title='Group')
