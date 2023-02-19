from flask import Blueprint, jsonify, request, current_app, redirect
from app.models import Class, Resource
from werkzeug.utils import secure_filename
from bson.binary import Binary
from bson.objectid import ObjectId
from app.utils import bad_request_code
from flask_cors import CORS
import json

import os

class_bp = Blueprint('class', __name__, url_prefix='/classes')
CORS(class_bp)


# create class
@class_bp.route('/', methods=['POST'])
def create_class():
    # resource can be url or file or both
    allowed_extensions = ['pdf', 'docx']
    file_extension_to_type = {
        'docx': 'DOCX_FILE',
        'pdf': 'PDF_FILE'
    }

    session_id = None

    if request.args.get('session_id') is None:
        return jsonify({
            'error': 'Query arguments should contain session_id e.g http://mindscape.com/classes/?session_id=abc'
        }), bad_request_code

    session_id = request.args.get('session_id')

    if request.form.get('name') is None:
        return jsonify({
            'error': 'Form data should contain class name'
        }), bad_request_code

    user_class = Class(name=request.form.get('name'), session_id=ObjectId(session_id))

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']

        if allowed_file(file.filename):
            valid_file_added = True
            filename = secure_filename(file.filename)
            file_extension = file.filename.split('.')[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            file_type = file_extension_to_type[file_extension]
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), "rb") as f:
                file_data = Binary(f.read())

            user_class.resources.append(Resource(type=file_type, url=filename, data=file_data))

    if request.form.get('vidLink'):
        user_class.resources.append(Resource(type='YOUTUBE',url=request.form.get('vidLink')))

    print(user_class.resources)

    user_class.save()

    return redirect('http://localhost:3000/class/' + str(user_class.id), 302)


# get classes by session
@class_bp.route('/', methods=['GET'])
def get_classes(session_id):
    if request.args.get('session_id') is not None:
        classes = Class.objects(session_id=ObjectId(session_id))
        results = []
        for mindscape_class in classes:
            results.append(mindscape_class.client_json())
        return jsonify({
            'data': results
        })
    else:
        return jsonify({
            'error': 'Include session id'
        }), bad_request_code

# get individual class
@class_bp.route('/<class_id>', methods=['GET'])
def get_class(class_id):
    user_class = Class.objects(_id=ObjectId(class_id)).first()

    if user_class is None:
        return jsonify({
            'error': 'class does not exist'
        }), 404

    return jsonify(json.loads(user_class.client_json())), 200

@class_bp.route('/<class_id>/', methods=['PUT'])
def add_resource(class_id):
    # resource can be url or file or both
    allowed_extensions = ['pdf', 'docx']
    file_extension_to_type = {
        'docx': 'DOCX_FILE',
        'pdf': 'PDF_FILE'
    }

    user_class = Class.objects(_id=ObjectId(class_id))

    if request.form.get('name') is not None:
        user_class.name = request.form.get('name')

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions

    if 'file' in request.files and request.files['file'].filename != '':
        file = request.files['file']

        if allowed_file(file.filename):
            valid_file_added = True
            filename = secure_filename(file.filename)
            file_extension = file.filename.split('.')[1]
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            file_type = file_extension_to_type[file_extension]
            with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), "rb") as f:
                file_data = Binary(f.read())

            user_class.resources.append(Resource(type=file_type, url=filename, data=file_data))

    if request.form.get('vidLink'):
        user_class.resources.append(Resource(type='YOUTUBE', url=request.form.get('vidLink')))

    user_class.save()

    return jsonify({
        'message': 'Resources uploaded successfully'
    })


# [
#     {
#         'question': 'what is 1+1?',
#         'answer': 1,
#         'options': [
#             '3',
#             '2',
#             '1',
#             '0'
#         ]
#     },
# {
#         'question': 'what is 1+1?',
#         'answer': 1,
#         'options': [
#             '3',
#             '2',
#             '1',
#             '0'
#         ]
#     }
# ]


@class_bp.route('/<class_id>/generate-quiz', methods=['POST'])
def generate_quiz(class_id):
    """
    building a qa bot with GPT3
    - tokenize the knowledge base - use tiktoken
    -
    """
    user_class = Class.objects(_id=ObjectId(class_id))

    if len(user_class.resources) == 0:
        return jsonify({
            'error': 'No resources to generate quizzes from!',
        })
    return jsonify([
        {
            'q': 'What is an OS?',
            'a': 1,
            'options': [
                'a',
                'b',
                'c',
                'd'
            ]
        }
    ])


@class_bp.route('/<class_id>/generate-flashcards', methods=['POST'])
def generate_flashcards(class_id):
    return jsonify([
        {
            'front': 'A fixed size entity in memory that can be placed in a frame on disk',
            'back': 'A Page'
        }
    ])


@class_bp.route('/<class_id>/generate-mindmap', methods=['POST'])
def generate_mindmaps(class_id):
    return jsonify([
        {
            'front': 'A fixed size entity in memory that can be placed in a frame on disk',
            'back': 'A Page'
        }
    ])
