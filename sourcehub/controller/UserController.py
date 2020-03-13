# from sourcehub import app
from flask import Blueprint, request, render_template, url_for, redirect, flash
from sourcehub.models import User
from flask_login import login_user, login_required, logout_user
from sourcehub.forms import RegistrationForm, LoginForm

user = Blueprint('user', __name__, url_prefix='/user')

@user.route('/<username>')
def index(username):
    '''
    个人用户主页
    '''

@user.route('/home')
def home():
    '''
    已登录用户主页
    '''
    pass

@user.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.register(form.data)
            if user:
                flash("注册成功！")
                User.login(form.data)
            else:
                flash("注册失败！")
            return redirect(url_for('index.main'))
        else:
            flash(form.errors)
            return redirect(url_for('user.register'))
    else:
        return render_template('user/register.html', form=form)


@user.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            print(request.form)
            user = User.login(form.data)
            if user:
                flash("登陆成功！")
                next = request.args.get('next')
                return redirect(next or url_for('index.main'))
            else:
                flash("登陆失败！")
                return redirect(url_for('user.login'))
        else:
            flash(form.errors)
            current_app.logger.debug(form.errors)
            return redirect(url_for('user.login'))
    else:
        return render_template('user/login.html', form=form)


@user.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("退出成功！")
    return redirect(url_for('index.main'))
