from flask import Blueprint, jsonify
from flask_cors import CORS

blueprint = Blueprint('home', __name__)
CORS(blueprint)

@blueprint.route('/')
def index():
    return jsonify({
        "message": "hello!"
    })
