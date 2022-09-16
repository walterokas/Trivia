import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

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

    def test_get_questions(self):
        res = self.client().get('/questions')

        self.assertEqual(res.status_code, 200)

    def test_delete_question(self):
        res = self.client().get('/questions/<int:id>')

        self.assertEqual(res.status_code, 200)

    def test_add_question(self):
        res = self.client().get('/questions/add')

        self.assertEqual(res.status_code, 200)

    def test_search_questions(self):
        res = self.client().get('/questions/search')

        self.assertEqual(res.status_code, 200)

    def test_get_questions_based_on_category(self):
        res = self.client().get('/category/<int:id>/questions')

        self.assertEqual(res.status_code, 200)

    def test_play_quiz(self):
        res = self.client().get('/quizzes')

        self.assertEqual(res.status_code, 200)
        # self.assert(len(res) >= 1)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()