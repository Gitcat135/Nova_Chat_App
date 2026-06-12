from app import app
from flask import render_template
from app.forms import SignInForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Index URL"""
    return render_template('index.html', title='Home Page')

@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    """Sign In URL"""
    form = SignInForm()
    return render_template('sign_in.html', title='Sign In Page', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register URL"""
    
    return render_template('register.html', title='Register Page')