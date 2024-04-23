from flask import Flask, render_template, redirect, session, flash
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

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register form for users"""

    form = RegistrationFrom()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        exiting_user = User.query.filter_by(username=username).first()
        if exiting_user:
            flash('User already exists. Please choose different username.', 'error')
            return redirect('/register')

        new_user = User.register(username, password, email, first_name, last_name)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = new_user.username
        return redirect('/secret')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login form for users"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect('/secret')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    session.pop('username', None)
    return redirect('/')

@app.route('/secret')
def secret():
    """Secret route"""
    if 'username' not in session:
        return redirect('/register')
    return render_template('secret.html')





if __name__ == '__main__':
    app.run(debug=True)