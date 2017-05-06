from functools import wraps
from flask import g, request, redirect, url_for, abort
from flask_login import current_user
from nexnest import logger

from nexnest.models.tour import Tour


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
        if 'tourID' in kwargs:
            tour = Tour.query.filter_by(id=int(kwargs['tourID'])).first()

            if tour is None:
                abort(404)

            if not tour.isEditableBy(g.user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function
