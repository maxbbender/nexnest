from nexnest import db
from nexnest.models.school import School
from flask import current_app as app

session = db.session


def allSchoolsAsStrings():
    app.logger.debug("allSchoolsAsStrings()")
    allSchools = session.query(School).all()

    app.logger.debug("allSchools : %r" % allSchools)

    schoolStringArray = []

    for school in allSchools:
        schoolStringArray.append(school.name)

    return schoolStringArray


def allSchools():
    app.logger.debug('allSchoolsAsStringsWithCord()')

    allSchools = School.query.all()

    schoolDictArray = []

    for school in allSchools:
        schoolDictArray.append(school.serialize)

    return schoolDictArray
