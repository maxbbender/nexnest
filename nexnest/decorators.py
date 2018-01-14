from functools import wraps
from flask import g, request, redirect, url_for, abort, flash
from flask_login import current_user

from nexnest.models.tour import Tour
from nexnest.models.group import Group
from nexnest.models.user import User
from nexnest.models.rent import Rent
from nexnest.models.listing import Listing
from nexnest.models.transaction import *


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

            if len(tour.listing.house) == 1:
                flash('Tours for this listing have been canceled as it already has tenants! Sorry!', 'warning')
                return redirect(url_for('indexs.index'))

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

            if len(tour.listing.house) == 1:
                flash('Tours for this listing have been canceled as it already has tenants! Sorry!', 'warning')
                return redirect(url_for('indexs.index'))

        return f(*args, **kwargs)
    return decorated_function


def group_editable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'groupID' in kwargs:
            group = Group.query.filter_by(id=int(kwargs['groupID'])).first()

            if group is None or not group.active:
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

            if group is None or not group.active:
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


def rent_editable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rentID' in kwargs:
            rent = Rent.query.filter_by(id=int(kwargs['rentID'])).first()

            if rent is None:
                abort(404)

            if not rent.isEditableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def rent_viewable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'rentID' in kwargs:
            rent = Rent.query.filter_by(id=int(kwargs['rentID'])).first()

            if rent is None:
                abort(404)

            if not rent.isViewableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def listing_viewable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'listingID' in kwargs:
            listing = Listing.query.filter_by(id=int(kwargs['listingID'])).first()

            if listing is None:
                abort(404)

            if not listing.isViewableBy(current_user, False):
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def listing_editable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'listingID' in kwargs:
            listing = Listing.query.filter_by(id=int(kwargs['listingID'])).first()

            if listing is None:
                abort(404)

            if not listing.isEditableBy(current_user, False) and not current_user.isAdmin:
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def listing_transaction_editable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'listingTransactionID' in kwargs:
            listingTransaction = ListingTransaction.query.filter_by(id=int(kwargs['listingTransactionID'])).first()

            if listingTransaction is None:
                abort(404)

            if not listingTransaction.isEditableBy(current_user) and not current_user.isAdmin:
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def listing_transaction_viewable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'listingTransactionID' in kwargs:
            listingTransaction = ListingTransaction.query.filter_by(id=int(kwargs['listingTransactionID'])).first()

            if listingTransaction is None:
                abort(404)

            if not listingTransaction.isViewableBy(current_user) and not current_user.isAdmin:
                abort(403)

        return f(*args, **kwargs)
    return decorated_function


def listing_cloneable(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'listingID' in kwargs:
            listing = Listing.query.filter_by(id=int(kwargs['listingID'])).first()

            if listing is None:
                abort(404)

            if not listing.isCloneableBy(current_user) and not current_user.isAdmin:
                abort(403)

        return f(*args, **kwargs)
    return decorated_function
