from mongoengine import StringField, EmbeddedDocumentListField
from app.models.mindscape_class import Class

from app.db import db


# A user session encapsulates each a duration of time for which a user interacts with the system
# When a user fills in the questionnaire, we create a user session which stores user's classes, learning preference
# We also show users their session ID so they can log in if they remember their session ID

class UserSession(db.Document):
    meta = {'collection': 'user_session'}
    learning_pref = StringField() # VIS - Visual, AUD - Auditory, SOC - social

    def client_json(self):
        return {
            'id': str(self.id),
            'learning_pref': self.learning_pref
        }



