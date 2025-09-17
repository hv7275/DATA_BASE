from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
from wtforms import StringField, PasswordField, SubmitField, EmailField

class RegistrationForm(FlaskForm):
  username = StringField(
    'User Name: ',
    validators=[DataRequired(), Length(min=5, max=20)]
  )
  
  first_name = StringField(
    'First Name: ',
    validators=[DataRequired(), Length(min=3, max=30)]
  )
  
  last_name = StringField(
    'Last Name: ',
    validators=[DataRequired(), Length(min=3, max=30)]
  )
  
  email = EmailField(
    'Email Id: ', 
    validators=[DataRequired(), Email()]
  )
  
  phone = StringField(
    'Phone No:',
    validators=[DataRequired(),
                Regexp(r'^\+?\d{10,15}$', message="Enter a valid phone number")]
  )
  
  password1 = PasswordField(
    'Password: ',
    validators=[DataRequired(), Length(min=6, max=20)]
  )
  password2 = PasswordField(
    'Confirm Password: ',
    validators=[
      DataRequired(), 
      Length(min=6, max=20), 
      EqualTo('password1', message='Passwords must match')
      ]
    )
  
  submit = SubmitField('Register')