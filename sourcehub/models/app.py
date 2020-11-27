# from mongoengine import Document, StringField, ListField, IntField, DateTimeField, ReferenceField
from sourcehub import db

class App(db.Model):
    __tablename__ = 'app'
    id = db.Column(db.Integer, primary_key = True)
    appid = db.Column(db.String(255), unique=True)
    appkey = db.Column(db.String(255))
    appmaster = db.Column(db.String(255))
