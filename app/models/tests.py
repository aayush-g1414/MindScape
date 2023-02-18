from mongoengine import StringField

from app.db import db


class TestDoc(db.Document):
    meta = {'collection': 'testdoc'}
    name = StringField()
    message = StringField()

