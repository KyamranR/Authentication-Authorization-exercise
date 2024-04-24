from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

class RegistrationFrom(FlaskForm):
    """User registration form"""

    username = StringField('Username:', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=6, max=50)])
    email = StringField('Email:', validators=[InputRequired(), Length(max=50)])
    first_name = StringField('First Name:', validators=[InputRequired(), Length(max=30)])
    last_name = StringField('Last Name:', validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """User login form"""

    username = StringField('Username:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """User feedback form"""
    
    title = StringField('Title', validators=[InputRequired()])
    content = TextAreaField('Content', validators=[InputRequired()])