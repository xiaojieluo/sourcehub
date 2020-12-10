from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text
from sqlalchemy.dialects import postgresql
from sourcehub.database import MutableList, ModelMixin, db


class Tag(ModelMixin, db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    sites = db.Column(
        MutableList.as_mutable(postgresql.ARRAY(db.Integer)),
        server_default='{}',
        default=list(),
    )

    links = db.Column(
        MutableList.as_mutable(postgresql.ARRAY(db.Integer)),
        server_default='{}',
        default=list(),
    )

    # 操作日志字段
    # log = db.Column(
    #     MutableList.as_mutable(postgresql.ARRAY(db.String(255))),
    #     default=list(),
    #     server_default='{}'
    # )

    @staticmethod
    def add(cls, obj: object, tags: list):
        for tag in tags:
            t = cls.query.filter_by(name=tag).first()
            if t is None:
                t = Tag(name=tag, sites=[obj.id,])
            else:
                t.sites.append(obj.id)

            db.session.add(t)
            db.session.commit()

            obj.tags.append(t.id)
            db.session.commit()