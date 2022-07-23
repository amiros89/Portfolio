from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from sqlalchemy.pool import NullPool
import os
from consts import LOCAL_RUN

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SECURITY_PASSWORD_SALT'] = 'salt'
Bootstrap(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SERVER_NAME'] = os.environ.get("SERVER_NAME", "127.0.0.1:5000")
login_manager = LoginManager(app)
login_manager.init_app(app)
app.config['MAIL_SERVER'] = 'smtp.sendgrid.net'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_DEFAULT_SENDER")
app.config['MAIL_USE_TLS'] = True
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"poolclass": NullPool}

if LOCAL_RUN:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('POSTGRES')
    app.config['MAIL_USERNAME'] = 'user'
    app.config['MAIL_PASSWORD'] = 'password'
    app.config['MAIL_DEFAULT_SENDER'] = 'email@email.com'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
