from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, URL
from consts import CHOICES

class RegisterForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired()])
    plan = SelectField("Plan", validators=[DataRequired()], choices=["Free", "Entrepreneur", "Tycoon"])
    submit = SubmitField("Sign me up")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Get me in")


class EbayQueryForm(FlaskForm):
    url = StringField("eBay URL", validators=[DataRequired(), URL()])
    num_of_ebay_items = SelectField("Number of sellers to extract from provided URL",choices=CHOICES,default="All")
    num_of_seller_top_selling = SelectField("Number of items from each seller in provided URL",choices=CHOICES,default="All")
    num_of_days_of_recent_sales = SelectField("Number of days to check for recent sales",choices=CHOICES,default="30")
    num_of_days_of_most_recent_sales = SelectField("Number of days to check for most recent sales",choices=CHOICES,default="7")
    num_of_sales_in_recent_days = SelectField("Times sold in recent days",choices=CHOICES,default="5")
    num_of_sales_in_most_recent_days = SelectField("Times sold in most recent days",choices=CHOICES,default="1")
    submit = SubmitField("Run Query")


class AmazonQueryForm(FlaskForm):
    url = StringField("Amazon URL", validators=[DataRequired(), URL()])
    submit = SubmitField("Run Query")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class EmailForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField("New Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm New Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class UserSettings(FlaskForm):
    email_notifications = BooleanField("Email Notifications")
    submit = SubmitField("Save Settings")
