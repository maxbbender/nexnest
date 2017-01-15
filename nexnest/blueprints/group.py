from flask import Blueprint
from flask import render_template, abort, request, redirect, url_for, flash, jsonify
from flask_login import current_user

from ..forms.createGroup import CreateGroupForm
from ..forms.inviteGroup import InviteGroupForm
from ..forms.suggestListingForm import SuggestListingForm

from nexnest.application import session

from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_listing import GroupListing
from nexnest.models.user import User
from nexnest.models.listing import Listing

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
    groupListings = group.suggestedListings
    #fake array of messages
    messages= [
        {
            'id': 0,
            'user': {'fname': 'Max', 'lname': 'Bender'},
            'content': 'Hey Mike we need a good way to test out messages',
            'date_created': '2017-01-14 23:09:41.536781'
        },
        {
            'id': 1,
            'user': {'fname': 'Mike', 'lname': 'McGinnis'},
            'content': 'Let me throw something together, any ideas?',
            'date_created': '2017-01-14 23:10:41.536781'
        },
        {
            'id': 2,
            'user': {'fname': 'Max', 'lname': 'Bender'},
            'content': 'Whatever you think',
            'date_created': '2017-01-14 23:11:41.536781'
        },
        {
            'id': 3,
            'user': {'fname': 'Mike', 'lname': 'McGinnis'},
            'content': 'Ill play around with it see what looks best. Ill try a new tab',
            'date_created': '2017-01-14 23:12:41.536781'
        },
        {
            'id': 4,
            'user': {'fname': 'Max', 'lname': 'Bender'},
            'content': 'Great cant wait to see!',
            'date_created': '2017-01-14 23:13:41.536781'
        },
        {
            'id': 5,
            'user': {'fname': 'Kyle', 'lname': 'Gavalchin'},
            'content': 'This looks amazing, youre so talented mike!',
            'date_created': '2017-01-14 23:14:41.536781'
        }
    ]

    form = InviteGroupForm()

    if group in current_user.accepted_groups:
        return render_template('group/viewGroup.html', group=group, suggestedListings=groupListings, messages=messages, invite_form=form)
    else:
        flash("You are not able to view a group you are not a part of")
        return redirect(url_for('indexs.index'))


@groups.route('/myGroups', methods=['GET', 'POST'])
def myGroups():
	groupsImIn = current_user.accepted_groups
	groupsImInvitedTo = current_user.un_accepted_groups
	return render_template('group/myGroups.html', 
							acceptedGroups=groupsImIn, 
							invitedGroups=groupsImInvitedTo, 
							title='My Groups')

@groups.route('/group/invite', methods=['POST'])
def invite():

    if request.method == 'POST':
        form = InviteGroupForm(request.form)
        print("@groups.invite() form.group_id.data : %s" % form.group_id.data)
        if form.validate():
            group = session.query(Group).filter_by(id=int(form.group_id.data)).first()
            user = session.query(User).filter_by(id=int(form.user_id.data)).first()
            newGroupUser = GroupUser(group, user)

            session.add(newGroupUser)
            session.commit()
        else:
            flash("Errors validating Group Invite form", 'danger')

    return redirect(url_for('groups.viewGroup', group_id=form.group_id.data))

@groups.route('/suggestListing', methods=['POST'])
def suggestListing():
    if request.method == 'POST':
        form = SuggestListingForm(request.form)
        if form.validate():
            group = session.query(Group).filter_by(id=int(form.group_id.data)).first()
            listing = session.query(Listing).filter_by(id=int(form.listing_id.data)).first()
            groupListing = session.query(GroupListing).filter_by(group_id=group.id, listing_id=listing.id).first()
            if not groupListing:
                newGroupListing = GroupListing(group, listing)
                session.add(newGroupListing)
                session.commit()
                flash("This listing has been suggested to " + group.name, 'info')
            else:
                flash("This listing has already been suggested to " + group.name + " by someone", 'info')
        else:
            flash("Errors validating Suggest Listing Invite form", 'danger')

    return redirect(url_for('listings.viewListing', listingID=form.listing_id.data))



