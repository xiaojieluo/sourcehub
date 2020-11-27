from sourcehub import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    sites = db.Column(db.ARRAY(db.Integer, dimensions = 1))
