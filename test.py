from nexnest.application import session

from nexnest.models.group import Group
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage

from nexnest.data_gen.factories import GroupFactory, UserFactory

g = GroupFactory()
u = UserFactory()

session.add(g)
session.add(u)

session.commit()

message = Message('hey', u, 'group')

session.add(message)

session.commit()

gm = GroupMessage(g, message)

session.add(gm)

session.commit()

print(gm)