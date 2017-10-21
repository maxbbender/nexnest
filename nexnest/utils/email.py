from threading import Thread
from flask_mail import Message
from nexnest import mail
# from flask import url_for
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer
from flask import current_app


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT']
        )
    except:
        return False
    return email


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body=None, html_body=None):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)

    if text_body is not None:
        msg.body = text_body

    if html_body is not None:
        msg.html = html_body

    if html_body is not None or text_body is not None:
        if not app.config['DEBUG']:
            # mail.send(msg)
            thr = Thread(target=send_async_email, args=[app, msg])
            thr.start()
        else:
            app.logger.debug('Sent Email ~ Subject: %s | Message %s' % (subject, html_body))
