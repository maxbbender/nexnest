from functools import wraps
from flask import g, request, redirect, url_for


def isLandlord(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not g.user.isLandlord:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function
