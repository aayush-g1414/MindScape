import os

from flask import Flask, jsonify
from flask_cors import CORS
from . import settings, controllers




project_dir = os.path.dirname(os.path.abspath(__file__))

def create_app(config_object=settings):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(config_object)

    from app.db import terminate_on_app_teardown, db
    db.init_app(app)

    terminate_on_app_teardown(app) # ensures we terminate db connection before returning response

    register_extensions(app)
    register_blueprints(app)

    register_errorhandlers(app)

    return app

def register_extensions(app):
    """Register Flask extensions."""
    # db.init_app(app)

    # with app.app_context():
        # db.create_all()
    return None

def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(controllers.home.blueprint)
    app.register_blueprint(controllers.tutorial.blueprint)
    app.register_blueprint(controllers.mindscape_class.class_bp)
    app.register_blueprint(controllers.session.session)
    return None

def register_errorhandlers(app):
    """Register error handlers."""
    @app.errorhandler(401)
    def internal_error(error):
        return jsonify({
            "message": "401 error!"
        }), 401

    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "message": "page does not exist!"
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            "message": "internal error occurred!"
        }), 500

    return None
