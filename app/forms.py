from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, Email, EqualTo


class SignInForm(FlaskForm):
    """Sign in form"""
    email = StringField('Email', render_kw={"placeholder": "you@example.com"}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={"placeholder": "Create a password"}, validators=[DataRequired()])
    remember_me = BooleanField('Keep me signed in')
    submit = SubmitField('Sign In')
    
class RegisterForm(FlaskForm):
    """Register form"""
    first_name = StringField('First Name', render_kw={"placeholder": "Jane"}, validators=[DataRequired(), length(min=2, max=20)])
    last_name = StringField('Last Name', render_kw={"placeholder": "Doe"}, validators=[DataRequired(), length(min=2, max=20)])
    username = StringField('Username', render_kw={"placeholder": "janedoe"}, validators=[DataRequired(), length(min=2, max=20)])
    email = StringField('Email', render_kw={"placeholder": "you@example.com"}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={"placeholder": "Min. 6 characters"}, validators=[DataRequired(), length(min=6, max=100)])
    confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm your password"}, validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')