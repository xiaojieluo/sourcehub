from flask import Blueprint, current_app
from flask_restful import Api, Resource, reqparse
from sourcehub.database import db
from sourcehub.models import App
from sqlalchemy.exc import IntegrityError

app_api = Blueprint('app_api', __name__)
api = Api(app_api)

class AppListApi(Resource):
    '''
    Token 操作列表
    '''
    def get(self):
        pass

    def post(self):
        """新建应用，传入x-sh-id, x-sh-key, x-sh-master
        """
        parser = reqparse.RequestParser()
        parser.add_argument('appid', type=str, help='input appid')
        parser.add_argument('appkey', type=str, help='input appkey')
        parser.add_argument('appmaster', type=str, help='input appmaster')
        args = parser.parse_args()
        current_app.logger.debug(args)

        try:
            application = App(**args)
            db.session.add(application)
            db.session.commit()
        except IntegrityError as e:
            # unique error
            db.session.rollback()
            current_app.logger.debug(e)
            return {
                'error_code': 1,
                'msg': f'有重复数据: {e.args}'
            }
        except Exception as e:
            db.session.rollback()
            current_app.logger.debug(e)

        return {
            'error_code': 0,
            'msg': 'success register application.',
            'data': {
                'appid': args['appid'],
                'appkey': args['appkey'],
                'appmaster': args['appmaster']
            }
        }

api.add_resource(AppListApi, '/')