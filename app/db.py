from flask_mongoengine import MongoEngine
from flask import current_app, g

db = MongoEngine()

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def terminate_on_app_teardown(app):
    app.teardown_appcontext(close_db)
