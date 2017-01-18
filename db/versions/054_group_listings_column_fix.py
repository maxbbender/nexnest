from sqlalchemy import *
from migrate import *


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    # users = Table('users', meta, autoload=True)
    gl = Table('group_listings', meta, autoload=True)

    gl.c.show.drop()

    group_show = Column("group_show", Boolean())
    landlord_show = Column("landlord_show", Boolean())
    req_description = Column("req_description", Text())

    group_show.create(gl)
    landlord_show.create(gl)
    req_description.create(gl)
    pass


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    gl = Table('group_listings', meta, autoload=True)

    gl.c.group_show.drop()
    gl.c.landlord_show.drop()
    gl.c.req_description.drop()

    show = Column("show", Boolean())

    show.create(gl)
    pass
