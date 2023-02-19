import openai
from app.prompts.generate_quiz import prompt
import json

import os


openai.api_key = os.getenv('OPEN_AI_API_KEY')

class QuizGen:
    @staticmethod
    def generate_quiz_questions(notes):
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt + notes,
            temperature=0.25
        )

        response = json.loads(response)

        return response
