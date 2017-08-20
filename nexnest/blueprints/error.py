from flask import Blueprint, render_template

errors = Blueprint('errors', __name__, template_folder='../templates/errors')


@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@errors.app_errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@errors.app_errorhandler(403)
def permissions_error(error):
    return render_template('403.html'), 403
