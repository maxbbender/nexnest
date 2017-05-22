from functools import wraps
from flask import g, request, redirect, url_for, abort
from flask_login import current_user
from nexnest import logger

from nexnest.models.tour import Tour
from nexnest.models.group import Group
from nexnest.models.user import User


def isLandlord(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.isLandlord:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def tour_editable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'tourID' in kwargs:
            tour = Tour.query.filter_by(id=int(kwargs['tourID'])).first()

            if tour is None:
                abort(404)

            if not tour.isEditableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def tour_viewable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'tourID' in kwargs:
            tour = Tour.query.filter_by(id=int(kwargs['tourID'])).first()

            if tour is None:
                abort(404)

            if not tour.isViewableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def group_editable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'groupID' in kwargs:
            group = Group.query.filter_by(id=int(kwargs['groupID'])).first()

            if group is None:
                abort(404)

            if not group.isEditableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def group_viewable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'groupID' in kwargs:
            group = Group.query.filter_by(id=int(kwargs['groupID'])).first()

            if group is None:
                abort(404)

            if not group.isViewableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def user_editable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'userID' in kwargs:
            user = User.query.filter_by(id=int(kwargs['userID'])).first()

            if user is None:
                abort(404)

            if not user.isEditableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function
