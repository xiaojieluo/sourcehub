# from nav import app
from nav.models import Tag, Link
from flask import Blueprint, render_template

tag = Blueprint('tag', __name__, url_prefix='/tag')

@tag.route('/<name>')
def index(name):
    # tags = Tag.find_all({'name': name})
    links = Link.objects(tags=name)
    tag_info = Tag.objects(name = name).first()
    print(tag_info)
    # tags = Link.find_all({'tag': })
    return render_template('tag/index.html', tag = tag_info, links = links)
