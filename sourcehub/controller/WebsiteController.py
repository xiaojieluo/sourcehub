from flask import Blueprint, request, render_template
from flask_login import login_required, current_user
from sourcehub.models import Site
from sourcehub.forms import CreateWebsiteForm

website = Blueprint('website', __name__, url_prefix='/website')


@website.route('/<id>', methods=['GET'])
def index(id):
    website = Site.objects(id=id).first()
    print(website)
    return render_template('website/index.html', website=website)


@website.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """收录网站

    Returns:
        [type] -- [description]
    """
    form = CreateWebsiteForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            author = current_user._get_current_object()
            data = {'author': author}
            data.update(form.data)

            # image = 
            website = Site.insert(data)
            print(website)
            return
            # link = Link.insert(data)
            if website:
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
        return render_template('website/create.html', form=form)
