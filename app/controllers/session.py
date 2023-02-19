from flask import Blueprint, jsonify, request, current_app
from app.models import UserSession
from app.utils import bad_request_code
from bson.objectid import ObjectId
from flask_cors import CORS


session = Blueprint('session', __name__, url_prefix='/sessions')
CORS(session)


@session.route('/', methods=['GET'])
def get_sessions():
    result = []
    for session in UserSession.objects:
        result.append(session.client_json())

    return jsonify(result)

@session.route('/<session_id>', methods=['GET'])
def get_session(session_id):
    user_session = UserSession.objects(pk=session_id).first()

    if user_session is None:
        return jsonify({
            'error': 'no such session!'
        }), 404

    return jsonify(user_session.client_json())


@session.route('/', methods=['POST'])
def create_session():
    req_body = request.get_json()
    if req_body['type'] not in ['VIS', 'SOC', 'AUD']:
        return jsonify({
            'error': 'Unidentified learning type. Must be one of VIS, SOC or AUD'
        }), bad_request_code

    new_session = UserSession(learning_pref=req_body['type'])

    new_session.save()

    return jsonify({
        "message": "Session successfully created!",
        'data': {
            'session_id': str(new_session.id)
        }
    })



