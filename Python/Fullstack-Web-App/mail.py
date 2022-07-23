from flask_mail import Mail, Message
from flask import url_for
from app import app
from threading import Thread
from db_classes import User

mail = Mail(app)
mail.init_app(app)


def async_function(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()

    return wrapper


@async_function
def send_query_ended(user_id):
    user = User.query.filter_by(id=user_id).first()
    user_name = user.name.split()[0]
    email = user.email
    with app.app_context():
        msg = Message('Hello from eLocator!',
                      recipients=[email])
        msg.html = f'<p>Hi {user_name}! This is for letting you know that your query has ended. Please follow this link to login and see all the goodies:</p>' \
                   f"<p><a href={url_for('login')}>Login</a></p>" \
                   '<br>' \
                   '<p>Thank you for using eLocator!</p>'
        mail.send(msg)


@async_function
def send_confirm_email(user_id, template):
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    with app.app_context():
        msg = Message(
            subject='Hello from eLocator!',
            recipients=[email],
            html=template
        )
        mail.send(msg)

@async_function
def send_reset_password_mail(user_id, template):
    user = User.query.filter_by(id=user_id).first()
    email = user.email
    with app.app_context():
        msg = Message(
            subject='Hello from eLocator!',
            recipients=[email],
            html=template
        )
        mail.send(msg)