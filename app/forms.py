from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, length, Email, EqualTo, ValidationError
from app.models import User


class SignInForm(FlaskForm):
    """Sign in form"""
    email = StringField('Email', render_kw={"placeholder": "you@example.com"}, validators=[DataRequired(), Email()])
    password = PasswordField('Password', render_kw={"placeholder": "Type your password"}, validators=[DataRequired()])
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
    submit = SubmitField('Create Account')

    def validate_username(self, username):
        """Validate new user username"""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        """Validate new user email"""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class PostForm(FlaskForm):
    """Post form"""
    body = StringField('Post', validators=[DataRequired(), length(min=1, max=500)])
    submit = SubmitField('Post')

class ResetPasswordRequestForm(FlaskForm):
    """Reset password request form"""
    email = StringField('Email', render_kw={"placeholder": "you@example.com"}, validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

class EditProfileForm(FlaskForm):
    """Edit Profile form"""
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    username = StringField('username')
    bio = TextAreaField('Bio', render_kw={"placeholder": "Tell the world a little about yourself..."})
    location = StringField('location', render_kw={"placeholder": "Nairobi, Kenya"})
    website = StringField('website', render_kw={"placeholder": "https://yourwebsite.com"})
    submit = SubmitField('Save Changes')

    def __init__(self, original_username, *args, **kwargs) -> None:
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user is not None:
                raise ValidationError('This username is already taken. Please choose a different one.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')