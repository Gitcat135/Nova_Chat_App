from app import app
from app.email import send_password_reset_email
from app.email import send_password_reset_email
from flask import render_template, flash, redirect, url_for, request
from app.forms import ResetPasswordRequestForm, SignInForm, RegisterForm, PostForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from app import db, app
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User, Post
from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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
        user = User(username=form.username.data, email=form.email.data, first_name=form.first_name.data, last_name=form.last_name.data)
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

@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    """Feed URL"""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    next_url = url_for('feed', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('feed', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('feed.html', title='Feed', posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)

@app.route('/profile' , methods=['GET', 'POST'])
@login_required
def profile():
    """Profile URL"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.author == current_user).paginate(
        page=page, per_page=app.config['POSTS_PER_PAGE'], error_out=False
    )
    next_url = url_for('profile', username=current_user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('profile', username=current_user.username, page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('profile.html', title=current_user.username, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)  
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.website.data = current_user.website
    return render_template('edit_profile.html', title=f'Edit Profile for {current_user.username}', form=form)


@app.route('/request_reset_password', methods=['GET', 'POST'])
def request_reset_password():
    """Request password reset URL"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # Redirect authenticated users to the index page
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)  # Send password reset email if user exists
            flash('Check your email for the instructions to reset your password.')
            return redirect(url_for('sign_in'))  # Redirect to sign in page after sending email
        
    return render_template('request_reset_password.html', title=' Request Password Reset ', form=form)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password URL"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template(
        'reset_password.html',
        title='Reset Password',
        form=form)