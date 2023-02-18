from mongoengine import *
from flask_mongoengine import MongoEngine
import json


class Quiz(EmbeddedDocument):
    # Quiz
    pass


class Resource(EmbeddedDocument):
    # Resource
    pass



class Class(Document):
    name = StringField()
    dateCreated = DateField()
    resources = ListField() # a list of Resource object
    flashcards = ListField()
    quizzes = EmbeddedDocumentField(Quiz)
    mindmap = StringField()

