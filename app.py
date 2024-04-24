from flask import Flask, render_template, redirect, session, flash, url_for
from models import db, connect_db, User, Feedback
from form import RegistrationFrom, LoginForm, FeedbackForm


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
        return redirect(url_for('logged_user'))

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
            return redirect(url_for('logged_user', username=user.username))
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout_user():
    session.pop('username', None)
    return redirect('/')

@app.route('/users/<username>')
def logged_user(username):
    """Logged in user information and show feedback"""
    if 'username' not in session or session['username'] != username:
        flash('You are not authorized to view this page, please login.', 'error')
        return redirect('/login')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return 'User not found.', 404
        
    feedbacks = Feedback.query.filter_by(username=username).all()
    return render_template('secret.html', user=user, feedbacks=feedbacks)
        
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Delete user and associated feedback"""
    if 'username' not in session or session['username'] != username:
        flash('You are not authorized to delete this user.', 'error')
        return redirect('/')
    
    user = User.query.filter_by(username=username).first()
    if not user:
        flash('User not found.', 'error')
        return redirect('/')
    
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    flash('User and associated feedback deleted successfully.', 'success')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Add new feedback"""

    if 'username' not in session or session['username'] != username:
        flash('You are not authorized to add feedback for this user.', 'error')
        return redirect('/')

    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback)
        db.session.commit()
        flash('Feedback added successfully.', 'success')
        return redirect(url_for('logged_user', username=username))
    return render_template('add_feedback.html', form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Update feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        flash('You are not authorized to update this feedback.', 'error')
        return redirect('/')
    
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        flash('Feedback updated successfully.', 'success')
        return redirect(url_for('user_profile', username=feedback.username))
    
    return render_template('update_feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback"""
    feedback = Feedback.query.get_or_404(feedback_id)
    if 'username' not in session or session['username'] != feedback.username:
        flash('You are not authorized to delete this feedback.', 'error')
        return redirect('/')
    
    db.session.delete(feedback)
    db.session.commit()
    flash('Feedback deleted successfully.', 'success')
    return redirect(url_for('user_profile', username=feedback.username))



if __name__ == '__main__':
    app.run(debug=True)