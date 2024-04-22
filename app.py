from flask import Flask, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'verysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """Rediredt to register form"""
    return redirect('/register')

@app.route('/register')
def register():
    """Register form for users"""
    

