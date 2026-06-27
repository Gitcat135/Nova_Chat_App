from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import SignInForm, RegisterForm
from app import db, app
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Index URL"""
    return render_template('index.html', title='Welcome')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    """Sign In URL"""
    form = SignInForm()
    if form.validate_on_submit():
        # Check if the user exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password. Please try again.')  # Flash an error message for
            return render_template('sign_in.html', title='Sign In', form=form)
        login_user(user, remember=form.remember_me.data)  # Log in the user
        flash(f'Welcome, {user.username}! You have successfully signed in.')  # Flash a success message
        return redirect(url_for('feed'))  # Redirect to Feed page after successful login
        
    return render_template('sign_in.html', title='Sign In Page', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register URL"""
    form = RegisterForm()
    if form.validate_on_submit():
        # Create a new user instance
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)  # Hash the password
        db.session.add(user)  # Add the user to the session
        db.session.commit()  # Commit the session to save the user to the database
        flash(f'Congratulations {form.username.data}, you are now a registered user!')  # Flash a success message
        return redirect(url_for('sign_in'))  # Redirect to sign in page after successful registration
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/feed')
def feed():
    """Feed URL"""
    return render_template('feed.html', title='Feed')

@app.route('/profile')
def profile():
    """Profile URL"""
    return render_template('profile.html', title='Profile')

@app.route('/edit_profile')
def edit_profile():
    """Edit Proflie URL"""
    return render_template('edit_profile.html', title='Edit Profile')