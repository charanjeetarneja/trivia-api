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
        self.assertEqual(output['message'], 'Page not found')

    def test_get_all_categories(self):
        response = self.client().get('/categories')
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["success"], True)
        self.assertTrue(output["categories"])

    def test_get_all_categories(self):
        response = self.client().get('/categories')
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["success"], True)
        self.assertTrue(output["categories"])

    def test_question_deletion(self):
        response = self.client().delete('/questions/4')
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["success"], True)

    def test_question_doesnt_exist_deletion(self):
        response = self.client().delete('/questions/99999')
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(output["success"], False)
        self.assertEqual(output["message"], "Page not found")

    def test_add_question(self):
        newQuestion = {
            'question': 'Test it?',
            'answer': 'Test',
            'difficulty': 4,
            'category': 4
        }
        response = self.client().post('/questions', json=newQuestion)
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output["success"], True)

    def test_search_questions(self):
        search = {'searchTerm': '?'}
        response = self.client().post('/search', json=search)
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output['success'], True)
        self.assertGreater(len(output['questions']), 0)

    def test_search_questions_not_found(self):
        search = {'searchTerm': 'test_search_questions_not_found'}
        response = self.client().post('/search', json=search)
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(output['success'], False)
        self.assertEqual(output['message'], 'Page not found')

    def test_questions_in_category(self):
        response = self.client().get('/categories/4/questions')
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output['success'], True)
        self.assertNotEqual(len(output['questions']), 0)
        self.assertGreater(output['totalQuestions'], 0)
        self.assertEqual(output['currentCategory'], 'History')

    def test_questions_in_category_not_found(self):
        response = self.client().get('/categories/999/questions')
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(output['success'], False)

    def test_quiz(self):
        quiz = {
            'previous_questions': [13],
            'quiz_category': {
                'type': 'Entertainment',
                'id': '3'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(output['success'], True)
        self.assertEqual(output['question']['category'], 3)

    def test_quiz_not_found_category(self):
        quiz = {
            'previous_questions': [6],
            'quiz_category': {
                'type': 'XXX',
                'id': 'X'
            }
        }
        response = self.client().post('/quizzes', json=quiz)
        output = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(output['success'], False)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()