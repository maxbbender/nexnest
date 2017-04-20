from flask import Blueprint, jsonify
from flask_login import login_required, current_user

from sqlalchemy import or_, and_

from nexnest import logger
from nexnest.application import session
from nexnest.models.notification import Notification

notifications = Blueprint('notifications', __name__, template_folder='../tempates/notification')


@notifications.route('/notification/<notifID>/read/AJAX')
@login_required
def markNotificationRead(notifID):
    notif = session.query(Notification).filter_by(id=notifID).first()

    errorMessage = None

    if notif is not None:
        if notif.isEditableBy(current_user, False):
            if not notif.viewed:
                notif.viewed = True
                session.commit()
            else:
                errorMessage = 'Notification already viewed'
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Notification does not exist'

    if errorMessage is not None:
        return jsonify(results={'success': False, 'message': errorMessage})
    else:
        return jsonify(results={'success': True})


@notifications.route('/notification/<notifID>/unRead/AJAX')
@login_required
def markNotificationUnRead(notifID):
    notif = session.query(Notification).filter_by(id=notifID).first()

    errorMessage = None

    if notif is not None:
        if notif.isEditableBy(current_user, False):
            if notif.viewed:
                notif.viewed = False
                session.commit()
            else:
                errorMessage = 'Notification already not viewed'
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = 'Notification does not exist'

    if errorMessage is not None:
        return jsonify(results={'success': False, 'message': errorMessage})
    else:
        return jsonify(results={'success': True})


@notifications.route('/notification/allRead')
@login_required
def markAllNotificationsRead():
    allUnreadNotifs = session.query(Notification) \
        .filter(Notification.target_user_id == current_user.id,
                Notification.viewed == False,
                Notification.category.in_(['generic_notification',
                                           'report_notification'])) \
        .all()

    logger.debug('All Unread Notifications %r' % allUnreadNotifs)

    for notif in allUnreadNotifs:
        # if notif.category not in ['generic_message, direct_message']:
        notif.viewed = True
        session.commit()

    return jsonify(results={'success': True})


@notifications.route('/messages/allRead')
@login_required
def markAllMessagesRead():
    allUnreadMessages = session.query(Notification) \
        .filter(Notification.target_user_id == current_user.id,
                Notification.viewed == False,
                Notification.category.in_(['generic_message',
                                           'direct_message'])) \
        .all()

    for messageNotif in allUnreadMessages:
        messageNotif.viewed = True
        session.commit()

    return jsonify(results={'success': True})


@notifications.route('/notification/<notifID>/allRead/AJAX')
@login_required
def markGroupedNotificationRead(notifID):
    logger.debug('/notification/<notifID>/allRead/AJAX')
    notif = Notification.query.filter_by(id=notifID).first()

    logger.debug('Looking at Notification : %r' % notif)
    logger.debug('Notification Details : %r' % notif.serialize)

    errorMessage = None
    if notif is not None:
        if notif.isEditableBy(current_user, False):
            allNotifsToMarkRead = Notification.query \
                .filter(Notification.redirect_url == notif.redirect_url,
                        Notification.notif_type == notif.notif_type,
                        Notification.target_user_id == current_user.id,
                        Notification.viewed == False) \
                .all()

            logger.debug('Other Notifications that matched queried : %r ' % allNotifsToMarkRead)

            if len(allNotifsToMarkRead) > 0:
                for notifa in allNotifsToMarkRead:
                    notifa.viewed = True
                    session.commit()
            else:
                errorMessage = "No notifications found to mark as read"
        else:
            errorMessage = 'Permissions Error'
    else:
        errorMessage = "Invalid Request"

    if errorMessage is not None:
        return jsonify(results={'success': False, 'message': errorMessage})
    else:
        return jsonify(results={'success': True})
