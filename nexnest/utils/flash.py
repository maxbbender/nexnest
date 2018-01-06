from flask import flash


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error), 'warning')


def flash_errors_json(form):
    messages = []

    for field, errors in form.errors.items():
        for error in errors:
            messages.append(u"Error in the %s field - %s" % (
                getattr(form, field).label.text, error))

    return messages