import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
from flask import session

from flaskr import create_app
from models import setup_db, Question, Category


#SETUP DATABASE CONNECTION CONFIG
#=========================================
database_name=os.getenv('DATABASE_NAME')
engine=os.getenv('ENGINE')
username=os.getenv('USERNAME')
password=os.getenv('PASSWORD')
domain=os.getenv('DOMAIN')
port=os.getenv('PORT')
database_path = f'{engine}://{username}:{password}@{domain}:{port}/{database_name}'

# RESOURCES https://flask.palletsprojects.com/en/2.2.x/testing/
# RESOURCES https://github.com/mjhea0/flaskr-tdd/blob/master/project/app.py
# RESOURCES https://dev.to/paurakhsharma/flask-rest-api-part-6-testing-rest-apis-4lla
# RESOURCES https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2019/testing-flask-applications-part-2/

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = database_name
        self.database_path = f'{engine}://{username}:{password}@{domain}:{port}/{database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_listCategories(self):
        res = self.client().get('/categories')

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res, None)

    def test_get_questions(self):
        res = self.client().get('/questions')
        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        res = self.client().delete('/questions/10', follow_redirects=True)
        print("Delete: ", res)
        self.assertEqual(res.status_code, 200)

        # Test Fail case
        res = self.client().delete('/questions/4', follow_redirects=True)
        print("Delete: ", res)
        self.assertEqual(res.status_code, 404)

    def test_add_question(self):
        res = self.client().post('/questions/add', 
            data = json.dumps({
                "question": "How are you today?",
                "answer": "Very well",
                "category": "2",
                "difficulty": "4"
                })
            )
        self.assertEqual(res.status_code, 200)

        # Test Fail Case
        res = self.client().post('/questions/add', 
            data = json.dumps({
                "question": "How are you today?",
                "answer": "Very well",
                "category": "",
                "difficulty": "4"
                })
            )
        self.assertEqual(res.status_code, 422)

    def test_search_questions(self):
        res = self.client().post('/questions/search', 
            data = json.dumps({
                "searchTerm": "the"
            })
        )
        self.assertEqual(res.status_code, 200)

        # Test Fail case
        res = self.client().post('/questions/search', 
            data = json.dumps({
                "searchTerm": ""
            })
        )
        self.assertEqual(res.status_code, 404)

    def test_get_questions_based_on_category(self):
        res = self.client().get('/categories/1/questions')
        self.assertEqual(res.status_code, 200)

        # Test Fail case
        res = self.client().get('/categories/15/questions')
        self.assertEqual(res.status_code, 500)

    def test_play_quiz(self):
        res = self.client().post('/quizzes', 
            data = json.dumps({
                "previous_questions": [1,2,3],
                "quiz_category": {"6": "Sports"}
            })
        )
        self.assertEqual(res.status_code, 200)

        # Test Fail case
        res = self.client().post('/quizzes', 
            data = json.dumps({
                "quiz_category": {"6": "Sports"}
            })
        )
        self.assertEqual(res.status_code, 500)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()