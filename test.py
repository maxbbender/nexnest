from nexnest.application import session

from nexnest.models.group import Group
from nexnest.models.user import User
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage
from nexnest.models.direct_message import DirectMessage

from nexnest.data_gen.factories import GroupFactory, UserFactory

from sqlalchemy import asc, or_, and_
u = session.query(User).filter_by(id=2).first()

print(u)
current_user = u
user_id = 3

dm = session.query(DirectMessage) \
    .filter(or_((and_(DirectMessage.source_user_id == current_user.id, DirectMessage.target_user_id == user_id)),
                (and_(DirectMessage.target_user_id == current_user.id, DirectMessage.source_user_id == user_id)))) \
    .order_by(asc(DirectMessage.date_created)) \
    .all()

# filter((DirectMessage.source_user_id == current_user.id &
#         DirectMessage.target_user_id == user_id) |
#        (DirectMessage.source_user_id == user_id &
#         DirectMessage.target_user_id == current_user.id)). \
# order_by(asc(DirectMessage.date_created)). \
# all()

print(dm)
