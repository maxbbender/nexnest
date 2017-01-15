from nexnest.application import session

from nexnest.models.group import Group
from nexnest.models.message import Message
from nexnest.models.group_message import GroupMessage

from nexnest.data_gen.factories import GroupFactory, UserFactory

g = session.query(Group).filter_by(id=1).first()

print(g.messages)

for gMessage in g.messages:
    print ("Message %i | Content %s" % (gMessage.id, gMessage.content))