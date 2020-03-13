from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo
from sourcehub.web import Unique
from sourcehub.models import User, Link


class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[
        DataRequired(),
        Length(min=4, max=25)
    ])
    email = StringField('Email Address:', validators=[
        DataRequired(),
        Length(min=6, max=35)
    ])
    password = PasswordField('Password:', [
        DataRequired(),
        EqualTo('password_confirm', message="Passwords must match.")
    ])
    password_confirm = PasswordField('Repeat Password:')


class LoginForm(FlaskForm):
    '''
    登陆表单
    '''
    email = StringField('Email Address:', validators=[
        DataRequired(),
        Length(min=6, max=35)
    ])
    password = PasswordField('Password:', [
        DataRequired()
    ])


class LinkForm(FlaskForm):
    '''
    链接表单
    '''
    url = StringField('Url:', [
        DataRequired(),
        Unique(Link, Link.url, message="该 url 已存在")
    ])
    tags = StringField('Tags:')
