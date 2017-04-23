from threading import Thread
from flask_mail import Message
from nexnest import app, mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body=None, html_body=None):
    msg = Message(subject, sender=sender, recipients=recipients)

    if text_body is not None:
        msg.body = text_body

    if html_body is not None:
        msg.html = html_body

    if html_body is not None or text_body is not None:
        thr = Thread(target=send_async_email, args=[app, msg])
        thr.start()
        # mail.send(msg)
