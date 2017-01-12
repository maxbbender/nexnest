from nexnest.application import session
from nexnest.models.user import User
from nexnest.models.group import Group

u = session.query(Group).filter_by(id=1).first()

# print(u)
# print(u.groups)
# print(u.accepted_groups)
# print(u.un_accepted_groups)

print(u.leader)