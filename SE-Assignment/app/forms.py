import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    IntegerField, DateField, SelectField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo,\
    Optional, InputRequired
from app.models import users_tbl, meals_tbl
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
# from app.models import User


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    date_of_birth = DateField('Date of birth')
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        email = users_tbl.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('This email has already been used to '
                                    'create an account please use another one')

    def validate_date_of_birth(form, field):
        if field.data > datetime.date(2004,1,1):
            raise ValidationError("Users must be born before 2004")


class QuestionnaireForm(FlaskForm):

    cooking_time = SelectField("How much time do you have to cook (mins)", choices=["30 or less", "60 or less"])
    meal_type = SelectField("What is your goal?", choices=["Gain muscle", "Loose weight", "Stay in shape"])
    meal_constraints = SelectField("Do you have any dietary preferences", choices=["High Carbs", "High protein",
                                                                                   "vegetarian", "None"])
    submit = SubmitField()


class UpdateUser(FlaskForm):

    user_name = StringField('Name', validators=[DataRequired()])
    user_email = StringField('User email')
    user_new_email = StringField('New email', validators=[DataRequired(), Email()])
    user_new_name = StringField('New name')
    user_date_of_birth = DateField('Date of birth')
    submit = SubmitField('Update details')

    def validate_email(self, user_email, user_new_email):
        user = users_tbl.query.filter_by(user_email=user_email).first()
        new_user = users_tbl.query.filter_by(user_email=user_new_email).first()
        if user and not new_user:
            raise ValidationError('User email already exists, please use a '
                                  'valid email')

    def validate_date_of_birth(form, field):
        if field.data > datetime.date(2004,1,1):
            raise ValidationError("Users must be born before 2004")

