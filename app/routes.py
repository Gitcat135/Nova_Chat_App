from app import app
from flask import render_template

@app.route('/')
@app.route('/index.html')
def index():
    """Index URL"""
    return render_template('index.html', title='Home page')
    