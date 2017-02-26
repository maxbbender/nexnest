from flask import Blueprint, jsonify
from flask import render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required

from nexnest.forms import CreateGroupForm, InviteGroupForm, SuggestListingForm, GroupMessageForm, GroupListingForm

from nexnest.application import session

# from nexnest.models import Group, GroupUser, GroupListing, User, Listing, GroupMessage, Tour, GroupListingFavorite
from nexnest.models.group import Group
from nexnest.models.group_user import GroupUser
from nexnest.models.group_listing import GroupListing
from nexnest.models.user import User
from nexnest.models.listing import Listing
from nexnest.models.group_message import GroupMessage
from nexnest.models.tour import Tour
from nexnest.models.group_listing_favorite import GroupListingFavorite

from nexnest.utils.flash import flash_errors

from sqlalchemy import asc, desc

groups = Blueprint('groups', __name__, template_folder='../templates')


@groups.route('/group/create', methods=['POST'])
@login_required
def createGroup():
    form = CreateGroupForm(request.form)

    if form.validate():
        # First we must check to make sure that the current_user
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
            flash('Group Created', 'success')

            return redirect(url_for('groups.viewGroup', group_id=newGroup.id))
        else:
            flash("Conflict with Group %s. Cannot create group in same time period as %s. Start(%s) End(%s)" %
                  (groupHasConflict.name,
                   groupHasConflict.name,
                   groupHasConflict.start_date,
                   groupHasConflict.end_date))

    return form.redirect()


@groups.route('/group/view/<group_id>')
@login_required
def viewGroup(group_id):
    # First lets check that the current user is apart of the group
    group = session.query(Group).filter_by(id=group_id).first()
    housingRequests = group.housingRequests

    invite_form = InviteGroupForm()
    message_form = GroupMessageForm(group_id=group_id)

    # Lets get the group's messages
    messages = session.query(GroupMessage). \
        filter_by(group_id=group.id). \
        order_by(desc(GroupMessage.date_created)).all()

    # Let's get the group's tours
    tours = session.query(Tour).filter_by(
        group_id=group.id).order_by(asc(Tour.last_requested)).all()

    if group in current_user.accepted_groups:

        return render_template('group/viewGroup.html',
                               group=group,
                               housingRequests=housingRequests,
                               favoritedListings=group.favorites,
                               invite_form=invite_form,
                               messages=messages,
                               tours=tours,
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
                return redirect(url_for('groups.viewGroup',
                                        group_id=form.group_id.data))
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

    return message_form.redirect()
    # return redirect(url_for('groups.viewGroup',
    #                         group_id=message_form.group_id.data))


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


@groups.route('/group/<groupID>/removeMember/<userID>')
@login_required
def removeMember(groupID, userID):
    group = session.query(Group) \
        .filter_by(id=groupID) \
        .first()

    if group is not None:
        if group.isEditableBy(current_user):
            groupUser = session.query(GroupUser) \
                .filter_by(group_id=groupID, user_id=userID) \
                .first()

            if groupUser is not None:
                groupUser.accepted = False
                groupUser.show = False
                session.commit()
            else:
                flash("User is not a part of the group", 'info')
    else:
        flash("Group does not exist", 'error')
        return redirect(url_for('indexs.index'))

    return redirect(url_for('groups.viewGroup', group_id=groupID))


@groups.route('/group/requestListing', methods=['POST'])
@login_required
def requestListing():
    rLForm = GroupListingForm(request.form)
    if rLForm.validate():
        group = session.query(Group) \
            .filter_by(id=rLForm.groupID.data) \
            .first()

        if group is not None:

            # Can the current user take actions on the group?
            if group.isEditableBy(current_user):
                listing = session.query(Listing) \
                    .filter_by(id=rLForm.listingID.data) \
                    .first()

                if listing is not None:
                    newGL = GroupListing(group=group,
                                         listing=listing,
                                         reqDescription=rLForm.reqDescription.data)
                    session.add(newGL)
                    session.commit()

                    return redirect(url_for('housingRequests.view', id=newGL.id))
                    flash("You have requested to live at this listing!", 'success')
                else:
                    flash("Listing does not exist", 'warning')
        else:
            flash("Group does not exist", 'warning')

    else:
        flash_errors(rLForm)

    return rLForm.redirect()


@groups.route('/group/<groupID>/favoriteListing/<listingID>', methods=['GET'])
@login_required
def favoriteListing(groupID, listingID):
    group = session.query(Group).filter_by(id=groupID).first()
    errorMessage = None
    favoriteCount = session.query(GroupListingFavorite) \
        .filter_by(group_id=groupID, listing_id=listingID)\
        .first()

    if favoriteCount is not None:

        group = session.query(Group).filter_by(id=groupID).first()
        listing = session.query(Listing).filter_by(id=listingID).first()

        if group is not None and listing is not None:
            if group.isViewableBy(user=current_user, flash=False):
                newGLF = GroupListingFavorite(group=group,
                                              listing=listing,
                                              user=current_user)
                session.add(newGLF)
                session.commit()

                return jsonify(results={'success': True})

            else:
                errorMessage = 'Permissions Error'
        else:
            errorMessage = 'Invalid Request'
    else:
        if not favoriteCount.show:
            favoriteCount.show = True
            return jsonify(results={'success': True})
        else:
            errorMessage = 'Listing has already been favorited by your group'

    return jsonify(results={'success': False, 'message': errorMessage})


@groups.route('/group/favoriteListing/<favoriteListingID>/show', methods=['GET'])
@login_required
def favoriteListingShow(favoriteListingID):
    favoriteListing = session.query(GroupListingFavorite) \
        .filter_by(id=favoriteListingID)\
        .first()

    if favoriteListing is not None:
        if favoriteListing.group.isEditableBy(user=current_user, flash=False):

            if not favoriteListing.show:
                favoriteListing.show = True
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
    favoriteListing = session.query(GroupListingFavorite) \
        .filter_by(id=favoriteListingID)\
        .first()

    if favoriteListing is not None:
        if favoriteListing.group.isEditableBy(user=current_user, flash=False):

            if favoriteListing.show:
                favoriteListing.show = False
                session.commit()
                return jsonify(results={'success': True})
            else:
                errorMessage = 'Favorited Listing has already been hidden'
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Invalid Request'

    return jsonify(results={'success': False, 'message': errorMessage})
