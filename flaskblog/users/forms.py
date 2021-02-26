from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    #between to qoute ('Username') it represented label in form .
    username = StringField('Username', 
            validators=[DataRequired(),Length(min=5,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password',
            validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

     # to confirm if the username or any field in form is validate 
     # must write the cartian syntax:

     # if validate_field(self, field):
        # if True:
                # raise ValidationError('validation message')

    def validate_username(self, username):
            userIsExist = User.query.filter_by(username=username.data).first()
            if userIsExist:
                    raise ValidationError('that username is taken. please choose anothor one')
    def validate_email(self, email):
            userIsExist = User.query.filter_by(email=email.data).first()
            if userIsExist:
                    raise ValidationError('that email is taken. please choose anothor one')
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    #between to qoute ('Username') it represented label in form .
    username = StringField('Username', 
            validators=[DataRequired(),Length(min=5,max=20)])
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
            if current_user.username != username.data:
                userIsExist = User.query.filter_by(username=username.data).first()
                if userIsExist:
                    raise ValidationError('that username is taken. please choose anothor one')

            
    def validate_email(self, email):
            if current_user.email != email.data:
                userIsExist = User.query.filter_by(email=email.data).first()
                if userIsExist:
                    raise ValidationError('that email is taken. please choose anothor one')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
            userIsExist = User.query.filter_by(email=email.data).first()
            if userIsExist is None:
                    raise ValidationError('There is no account with that email. You must register first.')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm password',
                            validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Reset Password')