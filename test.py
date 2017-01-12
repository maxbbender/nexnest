from nexnest.application import session
from nexnest.models.user import User

u = session.query(User).filter_by(username='fake1').first()

print(u)
print(u.accepted_groups)
print(u.un_accepted_groups)