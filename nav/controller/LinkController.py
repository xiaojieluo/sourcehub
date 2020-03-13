from flask import Blueprint
# from nav import app
from flask_login import login_required, current_user
from nav.models import Link

link = Blueprint('link', __name__, url_prefix='/link')

@link.route('/star/<linkid>')
@login_required
def star(linkid):
    '''将链接标星
    '''
    link = Link.objects(id = linkid).first()

    result = current_user.do_star(link)
    return {'result': 'True'}
