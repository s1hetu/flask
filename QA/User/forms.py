from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    profile_pic = StringField('Profile Image')
    register = SubmitField('Register')


class CreateTagForm(FlaskForm):
    name = StringField('Tag', validators=[DataRequired()])
    create = SubmitField('Create')


class AddressForm(FlaskForm):
    city = StringField('City',validators=[DataRequired()])
    state = StringField('State',validators=[DataRequired()])
    submit = SubmitField('Add address')

    def validate_state(self, state):
        if state.data == self.city.data:
            raise ValidationError("State and city cant be same.")
