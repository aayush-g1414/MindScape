from mongoengine import *
from flask_mongoengine import MongoEngine
import json
from app.db import db


class QuizQuestion(EmbeddedDocument):
    question = StringField()
    answer = IntField()
    options = ListField(StringField())
    user_answer = IntField() # -1 means the user never answered this.


class Quiz(EmbeddedDocument):
    questions = EmbeddedDocumentListField(QuizQuestion)
    date_completed = DateTimeField() # if user hasn't completed the quiz, we don't store any information here


class Resource(EmbeddedDocument):
    # Resource
    type = StringField(required=True) # YOUTUBE, PDF_FILE, DOCX_FILE
    url = StringField(required=True)
    data = BinaryField()
    # data - will be a string for urls and binary data for files


class FlashCard(EmbeddedDocument):
    front = StringField(required=True)
    back = StringField(required=True)


class Class(db.Document):
    meta = {'collection': 'classes'}
    _id = ObjectIdField()
    name = StringField(required=True)
    session_id = ObjectIdField(required=True)
    date_created = DateTimeField()
    resources = ListField(EmbeddedDocumentField(Resource)) # a list of Resource object
    flashcards = EmbeddedDocumentListField(FlashCard)
    quizzes = EmbeddedDocumentListField(Quiz)
    mind_map = StringField()

    def client_json(self):
        self_json = json.loads(self.to_json())
        return {
            'id': str(self._id),
            'name': self_json.name,
            'session_id': str(self.session_id),
            'date_created': self_json.date_created
        }
        # return {
        #     'id': str(self.id),
        #     'date_created': str(self.date_created),
        #     'resources': self.resources.
        #     'flashcards': self.flashcards.to_json(),
        #     'quizzes': self.quizzes.client_json(),
        #     'mind_map': self.mind_map.client_json()
        # }

