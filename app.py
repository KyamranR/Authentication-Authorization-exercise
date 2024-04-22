from flask import Flask, render_template, redirect
from models import db, connect_db, User
from form import RegistrationFrom, LoginForm

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

    form = RegistrationFrom()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name )
        db.session.add(new_user)
        db.session.commit()

        return redirect('/secret')
    return render_template('register.html', form=form)


