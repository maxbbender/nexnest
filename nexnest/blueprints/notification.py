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
