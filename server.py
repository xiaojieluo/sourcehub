from sourcehub import make_app
from flask_migrate import Migrate


if __name__ == '__main__':
    app = make_app()
    app.run(
        host='0.0.0.0',
        debug=True,
    )

# TODO
# manage command:
# clean database: 清除数据库冗余
#     清楚 tags 表中 count 为0 的表
