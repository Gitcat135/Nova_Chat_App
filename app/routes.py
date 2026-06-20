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
    return render_template('index.html', title='Home Page')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    """Sign In URL"""
    form = SignInForm()
    if form.validate_on_submit():
        # Check if the user exists in the database
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password. Please try again.')  # Flash an error message for
            return render_template('sign_in.html', title='Sign In Page', form=form)
        login_user(user, remember=form.remember_me.data)  # Log in the user
        flash(f'Welcome, {user.username}! You have successfully signed in.')  # Flash a success message
        return redirect(url_for('index'))  # Redirect to index page after successful login
        
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
    return render_template('register.html', title='Register Page', form=form)

@app.route('/logout')
def logout():
    """Logout URL"""
    logout_user()  # Log out the current user
    flash('You have been logged out.')  # Flash a message indicating successful logout
    return redirect(url_for('login'))  # Redirect to index page after logout