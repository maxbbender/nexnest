from nexnest.models.notification import Notification
from nexnest.application import session


def createNotification(targetUser, targetModelID, notifType):
    newNotification = Notification(target_user=targetUser,
                                   target_model_id=self.id,
                                   notif_type='group_message')

    session.add(newNotification)
    session.commit()
