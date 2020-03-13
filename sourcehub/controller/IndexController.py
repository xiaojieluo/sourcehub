# from sourcehub import app
from flask import Blueprint, request, render_template, flash, redirect, url_for, current_app
from sourcehub.models import User, Link
import pymongo
from sourcehub import define
from sourcehub.forms import LinkForm
from flask_login import login_required, current_user
from sourcehub.api import IndexApi

index = Blueprint('index', __name__, url_prefix='')


@index.route('/')
def main():
    links = Link.objects(is_show=1).order_by('created_at')

    index = IndexApi.index()
    s = index.get(12)
    return s

    return render_template('index/index.html', links=links)


@index.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = LinkForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            author = current_user._get_current_object()
            data = {'author': author}
            data.update(form.data)
            link = Link.insert(data)
            if link:
                flash("添加成功！")
                return redirect(url_for('index.main'))
            else:
                flash("添加错误")
                return redirect(url_for('index.create'))
        else:
            flash("添加错误:{}".format(form.errors))
            current_app.logger.debug(form.errors)
            return redirect(url_for('index.create'))
    else:
        return render_template('index/create.html', form=form)
