import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}@{}/{}".format("postgres:postgres", 'localhost', self.database_name)
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
    def test_get_page_of_questions(self):
        response = self.client().get('/questions')
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200,msg='Status Code is not 200')
        self.assertEqual(output["success"], True)
        self.assertTrue(output["totalQuestions"])
        self.assertGreaterEqual(len(output["categories"]),0)
        self.assertGreaterEqual(len(output["questions"]),0)
    
    def test_get_incorrect_page(self):
        response=self.client().get('/questions?page=122')
        output=json.loads(response.data)
        self.assertEqual(response.status_code,404)
        self.assertEqual(output["success"],False)
        self.assertEqual(output['message'], 'Bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()