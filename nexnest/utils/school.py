from nexnest.application import session
from nexnest.models.school import School
from nexnest import logger


def allSchoolsAsStrings():
    logger.debug("allSchoolsAsStrings()")
    allSchools = session.query(School).all()

    logger.debug("allSchools : %r" % allSchools)

    schoolStringArray = []

    for school in allSchools:
        schoolStringArray.append(school.name)

    return schoolStringArray
