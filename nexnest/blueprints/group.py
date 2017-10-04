from flask import (Blueprint, flash, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import current_user, login_required
from flask import current_app as app
from nexnest import db
from nexnest.decorators import group_editable, group_viewable
from nexnest.forms import (CreateGroupForm, GroupListingForm, GroupMessageForm,
                           InviteGroupForm, SuggestListingForm)
from nexnest.models.group import Group
from nexnest.models.group_email import GroupEmail
from nexnest.models.group_listing import GroupListing
from nexnest.models.group_listing_favorite import GroupListingFavorite
from nexnest.models.group_listing_message import GroupListingMessage
from nexnest.models.group_message import GroupMessage
from nexnest.models.group_user import GroupUser
from nexnest.models.house import House
from nexnest.models.listing import Listing
from nexnest.models.notification import Notification
from nexnest.models.tour import Tour
from nexnest.models.user import User
from nexnest.utils.email import send_email
from nexnest.utils.flash import flash_errors
from nexnest.utils.group import genGroupEmailInviteNoUser
from sqlalchemy import asc, desc

groups = Blueprint('groups', __name__, template_folder='../templates')

session = db.session


@groups.route('/group/create', methods=['POST'])
@login_required
def createGroup():

    if current_user.isLandlord:
        flash('Sorry! Landlords are unable to create groups.', 'warning')
        return redirect(url_for('landlords.dashboard'))

    form = CreateGroupForm(request.form)

    if form.validate():
        # First we must check to make sure that the current_user
        # isn't trying to create a group that conflicts with
        # other dates of groups user is a part of
        groupHasConflict = None
        conflict = False
        for group in current_user.accepted_groups:
            if form.time_frame == group.target_time_period:
                groupHasConflict = group
                conflict = True
                break

        if not conflict:
            newGroup = Group(name=form.name.data,
                             leader=current_user,
                             target_time_period=form.time_frame.data)

            session.add(newGroup)
            session.commit()

            flash('Group Created! Navigate to "My Groups" in your menu to view group and invite your future housemates', 'success')

            return form.redirect()
        else:
            flash("Conflict with Group %s. Cannot create group in same time period as %s. Start(%s) End(%s)" %
                  (groupHasConflict.name,
                   groupHasConflict.name,
                   groupHasConflict.target_time_period))

    return form.redirect()


@groups.route('/group/view/<groupID>')
@login_required
@group_viewable
def viewGroup(groupID):
    # First lets check that the current user is apart of the group
    group = Group.query.filter_by(id=groupID).first_or_404()

    housingRequests = group.housingRequests

    invite_form = InviteGroupForm()
    message_form = GroupMessageForm(group_id=groupID)
    message_form.next.data = url_for('groups.viewGroup', groupID=groupID)

    # Lets get the group's messages
    messages = session.query(GroupMessage). \
        filter_by(group_id=group.id). \
        order_by(desc(GroupMessage.date_created)).all()

    # Let's get the group's tours
    tours = session.query(Tour)\
        .filter_by(group_id=group.id, declined=False)\
        .order_by(asc(Tour.last_requested))\
        .all()

    house = session.query(House) \
        .filter_by(group_id=group.id) \
        .order_by(asc(House.date_created)) \
        .first()

    return render_template('group/viewGroup.html',
                           group=group,
                           housingRequests=housingRequests,
                           favoritedListings=group.displayedFavorites(),
                           invite_form=invite_form,
                           messages=messages,
                           tours=tours,
                           message_form=message_form,
                           house=house)


@groups.route('/group/invite', methods=['POST'])
@login_required
@group_editable
def invite():
    form = InviteGroupForm(request.form)
    if form.validate():
        group = Group.query.filter_by(
            id=int(form.group_id.data)).first_or_404()

        user = User.query.filter_by(id=int(form.user_id.data)).first_or_404()

        newGroupUser = GroupUser(group, user)

        session.add(newGroupUser)
        session.commit()

        newGroupUser.genNotifications()
        return form.redirect()
    else:
        flash_errors(form)
        return redirect(url_for('groups.viewGroup',
                                groupID=form.group_id.data))


@groups.route('/group/message/create', methods=['POST'])
@login_required
@group_viewable
def createMessage():
    message_form = GroupMessageForm(request.form)

    if message_form.validate():
        group = Group.query.filter_by(
            id=int(message_form.group_id.data)).first_or_404()

        newMessage = GroupMessage(group=group,
                                  user=current_user,
                                  content=message_form.content.data)

        session.add(newMessage)
        session.commit()

        newMessage.genNotifications()
    else:
        flash_errors(message_form)

    return message_form.redirect()


@groups.route('/group/leave/<groupID>')
@login_required
@group_viewable
def leaveGroup(groupID):
    groupToLeave = Group.query.filter_by(id=groupID).first_or_404()

    if current_user in groupToLeave.acceptedUsers:
        if current_user.leaveGroup(groupToLeave):
            flash("You have left %s" % groupToLeave.name, 'success')
            return redirect(url_for('indexs.index'))
        else:
            return redirect(url_for('groups.viewGroup',
                                    groupID=groupToLeave.id))

    if request.is_xhr:
        return jsonify({'success': True})
    else:
        return redirect(url_for('indexs.index'))


@groups.route('/group/<groupID>/assignLeader/<user_id>')
@login_required
@group_editable
def assignNewLeader(groupID, userID):
    group = Group.query.filter_by(id=groupID).first_or_404()
    group.leader_id = userID
    session.commit()

    return redirect(url_for('groups.viewGroup',
                            groupID=group.id))


@groups.route('/group/<groupID>/removeMember/<userID>')
@login_required
@group_editable
def removeMember(groupID, userID):
    groupUser = GroupUser.query.filter_by(group_id=groupID, user_id=userID) \
        .first_or_404()

    groupUser.accepted = False
    groupUser.show = False
    session.commit()

    return redirect(url_for('groups.viewGroup', groupID=groupID))


@groups.route('/group/<groupID>/favoriteListing/<listingID>', methods=['GET'])
@login_required
@group_viewable
def favoriteListing(groupID, listingID):
    favoriteCount = GroupListingFavorite.query \
        .filter_by(group_id=groupID, listing_id=listingID)\
        .first()

    errorMessage = None

    if not favoriteCount:
        group = Group.query.filter_by(id=groupID).first_or_404()
        listing = Listing.query.filter_by(id=listingID).first_or_404()
        newGLF = GroupListingFavorite(group=group,
                                      listing=listing,
                                      user=current_user)
        session.add(newGLF)
        session.commit()
    else:
        if not favoriteCount.show:
            favoriteCount.show = True
            return jsonify(results={'success': True})
        else:
            errorMessage = 'Listing has already been favorited by your group'

    if errorMessage is None:
        if request.is_xhr:
            return jsonify(results={'success': True})
        else:
            flash('Listing has been favorited', 'success')
            return redirect(url_for('groups.viewGroup', groupID=groupID))
    else:
        if request.is_xhr:
            return jsonify(results={'success': False, 'message': errorMessage})
        else:
            flash(errorMessage, 'success')
            return redirect(url_for('groups.viewGroup', groupID=groupID))


@groups.route('/group/favoriteListing/<favoriteListingID>/show', methods=['GET'])
@login_required
def favoriteListingShow(favoriteListingID):
    favoritedListing = session.query(GroupListingFavorite) \
        .filter_by(id=favoriteListingID)\
        .first()

    if favoritedListing is not None:
        if favoritedListing.group.isEditableBy(user=current_user, toFlash=False):

            if not favoritedListing.show:
                favoritedListing.show = True
                session.commit()
                return jsonify(results={'success': True})
            else:
                errorMessage = 'Favorited Listing is already showing'
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Request'

    return jsonify(results={'success': False, 'message': errorMessage})


@groups.route('/group/favoriteListing/<favoriteListingID>/hide', methods=['GET'])
@login_required
def favoriteListingHide(favoriteListingID):
    favoritedListing = session.query(GroupListingFavorite) \
        .filter_by(id=favoriteListingID)\
        .first()

    if favoritedListing is not None:
        if favoritedListing.group.isEditableBy(user=current_user, toFlash=False):

            if favoritedListing.show:
                favoritedListing.show = False
                session.commit()
                return jsonify(results={'success': True})
            else:
                errorMessage = 'Favorited Listing has already been hidden'
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Request'

    return jsonify(results={'success': False, 'message': errorMessage})


@groups.route('/group/<groupID>/inviteByEmail/<emailAddress>')
@login_required
@group_editable
def inviteUserByEmail(groupID, emailAddress):
    errorMessage = None
    group = Group.query.filter_by(id=groupID).first_or_404()

    # Let's see if the user is already part of the website
    user = User.query.filter_by(email=emailAddress).first()

    # First make sure this user hasn't already been invited by email
    groupEmailCheck = GroupEmail.query.filter_by(group=group, email=emailAddress).count()

    if user is not None:
        # Make sure user isn't already a part of the group
        groupUserCheck = GroupUser.query.filter_by(group=group, user=user).count()

        if groupUserCheck == 1:
            errorMessage = 'User is already a part of your group!'

    if groupEmailCheck > 0:
        app.logger.warning('User %r just tried to invite %s a second time' %
                           (current_user, emailAddress))
        errorMessage = 'You have already sent an invite to this email!'

    # No Errors
    if errorMessage is None:
        if user is None:
            message = genGroupEmailInviteNoUser(group)
        else:
            message = 'you are already a part of the site. here is the link to confirm'

        send_email(subject='NexNest - %s' % 'Group Invite',
                   sender='no_reply@nexnest.com',
                   recipients=[emailAddress],
                   html_body=render_template('email/emailTemplate.html',
                                             messageContent=message,
                                             icon='users',
                                             messageType='group invite'))

    if errorMessage is None:
        if request.is_xhr:
            return jsonify({'success': True})
        else:
            flash('Sent email to %s inviting them to your group!' %
                  emailAddress, 'success')
            return redirect(url_for('groups.viewGroup', groupID=groupID))
    else:
        if request.is_xhr:
            return jsonify({'success': False, 'message': errorMessage})
        else:
            flash(errorMessage, 'danger')
            return redirect(url_for('groups.viewGroup', groupID=groupID))


@groups.route('/group/confirmEmailInvite')
@login_required
def acceptEmailInvite():
    groupEmail = GroupEmail.query \
        .filter_by(email=current_user.email) \
        .first_or_404()

    groupUserCheck = GroupUser.query.filter_by(group=groupEmail.group, user=current_user).count()
    errorMessage = None
    if groupUserCheck == 0:
        newGroupUser = GroupUser(groupEmail.group, current_user)
        newGroupUser.accepted = True
        groupEmail.used = True
        newGroupUser.genCompletedNotifications()
        session.add(newGroupUser)
        session.commit()
    else:
        errorMessage = 'You are already a part of this group!'

    if errorMessage is None:
        if request.is_xhr:
            return jsonify({'success': True})
        else:
            flash('You have joined %s!' % groupEmail.group.name, 'success')
            return redirect(url_for('groups.viewGroup', groupID=groupEmail.group.id))
    else:
        if request.is_xhr:
            return jsonify({'success': False, 'message': errorMessage})
        else:
            flash(errorMessage, 'danger')
            return redirect(url_for('groups.viewGroup', groupID=groupEmail.group.id))


@groups.route('/group/deleteGroup/<groupID>')
@login_required
@group_editable
def deleteGroup(groupID):
    errorMessage = None
    group = Group.query.filter_by(id=groupID).first_or_404()

    # There can't be any users in the group if it is to be deleted
    if len(group.acceptedUsers) == 1:
        group.active = False
        group.leader_id = 1
        db.session.commit()
        flash('Your group %s has been deleted!' % group.name, 'success')
    else:
        errorMessage = 'You cannot delete %s because there are still other members in it. Delete them or assign a new group leader' % group.name

    if errorMessage is None:
        if request.is_xhr:
            return jsonify({'success': True})
        else:
            flash('Successfully deleted %s' % group.name, 'success')
            return redirect(url_for('indexs.index'))
    else:
        if request.is_xhr:
            return jsonify({'success': False, 'message': errorMessage})
        else:
            flash(errorMessage, 'danger')
            return redirect(url_for('indexs.index'))
