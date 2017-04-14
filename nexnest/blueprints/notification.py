from flask import Blueprint, jsonify
from flask_login import login_required, current_user

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
        .filter_by(target_user_id=current_user.id,
                   viewed=False) \
        .all()

    for notif in allUnreadNotifs:
        notif.viewed = True
        session.commit()

    return jsonify(results={'success': True})
