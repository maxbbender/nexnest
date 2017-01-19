from flask import Blueprint
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from ..forms.createGroup import CreateGroupForm
from ..forms.inviteGroup import InviteGroupForm
from ..forms.suggestListingForm import SuggestListingForm
from ..forms.createGroupMessageForm import GroupMessageForm

from nexnest.application import session

from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_listing import GroupListing
from nexnest.models.user import User
from nexnest.models.listing import Listing
from nexnest.models.group_message import GroupMessage

from nexnest.utils.flash import flash_errors

from sqlalchemy import asc

groups = Blueprint('groups', __name__, template_folder='../templates')


@groups.route('/group/create', methods=['GET', 'POST'])
@login_required
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

            newGroupUser = GroupUser(newGroup, current_user)

            session.add(newGroupUser)
            session.commit()

            return redirect(url_for('groups.viewGroup', group_id=newGroup.id))
        else:
            flash("Conflict with Group %s. Cannot create group in same time period as %s. Start(%s) End(%s)" %
                  (groupHasConflict.name,
                   groupHasConflict.name,
                   groupHasConflict.start_date,
                   groupHasConflict.end_date))

            return redirect(url_for('groups.createGroup'))
    else:
        return render_template('createGroup.html', form=form)


@groups.route('/group/view/<group_id>')
@login_required
def viewGroup(group_id):
    # First lets check that the current user is apart of the group
    group = session.query(Group).filter_by(id=group_id).first()
    groupListings = group.suggestedListings

    invite_form = InviteGroupForm()
    message_form = GroupMessageForm(group_id=group_id)

    # Lets get the group's messages
    messages = session.query(GroupMessage). \
        filter_by(group_id=group.id). \
        order_by(asc(GroupMessage.date_created)).all()

    if group in current_user.accepted_groups:

        return render_template('group/viewGroup.html',
                               group=group,
                               suggestedListings=groupListings,
                               invite_form=invite_form,
                               messages=messages,
                               message_form=message_form)

    else:
        flash("You are not a part of %s" % group.name, 'warning')
        return redirect(url_for('indexs.index'))


@groups.route('/group/invite', methods=['POST'])
@login_required
def invite():
    if request.method == 'POST':
        form = InviteGroupForm(request.form)
        print("@groups.invite() form.group_id.data : %s" % form.group_id.data)
        if form.validate():
            group = session.query(Group).filter_by(
                id=int(form.group_id.data)).first()

            # Is the current user apart of the group
            if group in current_user.accepted_groups:
                user = session.query(User) \
                    .filter_by(id=int(form.user_id.data)) \
                    .first()

                newGroupUser = GroupUser(group, user)

                session.add(newGroupUser)
                session.commit()
            else:
                flash("Unable to invite a user to a group you are not apart of",
                      'warning')
            return redirect(url_for('indexs.index'))
        else:
            flash_errors(form)
            return redirect(url_for('groups.viewGroup',
                                    group_id=form.group_id.data))


@groups.route('/group/message/create', methods=['POST'])
@login_required
def createMessage():
    message_form = GroupMessageForm(request.form)

    if message_form.validate():
        group = session.query(Group). \
            filter_by(id=message_form.group_id.data). \
            first()
        if group in current_user.accepted_groups:

            newMessage = GroupMessage(group=group,
                                      user=current_user,
                                      content=message_form.content.data)

            session.add(newMessage)
            session.commit()
        else:
            flash("Unable to post a message to a group you are not apart of",
                  'warning')
            return redirect(url_for('indexs.index'))
    else:
        flash_errors(message_form)

    return redirect(url_for('groups.viewGroup',
                            group_id=message_form.group_id.data))


@groups.route('/group/suggestListing', methods=['POST'])
@login_required
def suggestListing():

    if request.method == 'POST':
        form = SuggestListingForm(request.form)
        if form.validate():
            group = session.query(Group).filter_by(
                id=int(form.group_id.data)).first()

            # Is the current user apart of the group?
            if group in current_user.accepted_groups:
                listing = session.query(Listing).filter_by(
                    id=int(form.listing_id.data)).first()

                groupListing = session.query(GroupListing).filter_by(
                    group_id=group.id, listing_id=listing.id).first()

                if not groupListing:
                    newGroupListing = GroupListing(group, listing)
                    session.add(newGroupListing)
                    session.commit()
                    flash("This listing has been suggested to %s" %
                          group.name, 'info')
                else:
                    flash("This listing has already been suggested to " +
                          group.name + " by someone", 'info')
            else:
                flash("Unable to suggest a listing to a group you are not apart of",
                      'warning')
                return redirect(url_for('indexs.index'))
        else:
            flash("Errors validating Suggest Listing Invite form", 'danger')

    return redirect(url_for('listings.viewListing',
                            listingID=form.listing_id.data))


@groups.route('/group/leave/<groupID>')
@login_required
def leaveGroup(groupID):
    groupToLeave = session.query(Group) \
        .filter_by(id=groupID) \
        .first()

    groupUserCount = session.query(GroupUser) \
        .filter_by(group_id=groupToLeave.id,
                   user_id=current_user.id,
                   accepted=True) \
        .count()

    # Does the group exist?
    if groupToLeave is not None:
        # Is the user a part of the group?
        if groupUserCount == 1:
            if current_user.leaveGroup(groupToLeave):
                flash("You have left %s" % groupToLeave.name, 'success')
                return redirect(url_for('indexs.index'))
            else:
                return redirect(url_for('groups.viewGroup',
                                        group_id=groupToLeave.id))
        else:
            flash("You are not apart of %s" % groupToLeave.name, 'danger')
            return redirect(url_for('indexs.index'))
    else:
        flash("Group you are trying to leave doesn't exist", 'danger')
        return redirect(url_for('indexs.index'))


@groups.route('/group/<group_id>/assignLeader/<user_id>')
@login_required
def assignNewLeader(group_id, user_id):
    group = session.query(Group).filter_by(id=group_id).first()

    # Is the current user the leader of this group
    if group.leader_id == current_user.id:
        group.leader_id = user_id
        session.commit()
    else:
        flash("Only group leader can re-assign the leader", 'danger')

    return redirect(url_for('groups.viewGroup',
                            group_id=group.id))
