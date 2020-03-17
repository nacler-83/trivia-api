#  --------------------------------------------------------------------------#
#  Imports
#  --------------------------------------------------------------------------#


import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Question, Category


#  --------------------------------------------------------------------------#
#  Classes and Tests
#  --------------------------------------------------------------------------#


class TriviaTestCase(unittest.TestCase):
    # This class represents the trivia test case

    def setUp(self):
        # Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'trivia_test'
        self.database_path = 'postgresql://{}/{}'.format(
                             'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        # new question payload to be used in tests
        self.new_question = {
            "question": "What is the meaning of life?",
            "answer": "42",
            "difficulty": 2,
            "category": 4
        }
        # payload for play_game (/quizzes) endpoint test
        self.play_game = {
            "previous_questions": [16, 17],
            "quiz_category": {
                "type": "Art",
                "id": "2"
            }
        }
        # payload for play_game 404 (/quizzes) endpoint test
        self.play_game_404 = {
            "previous_questions": [16, 17],
            "quiz_category": {
                "type": "Art",
                "id": "100"
            }
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        # Executed after reach test
        pass

    #  test GET all the categories
    #  ----------------------------------------------------------------
    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    #  test GET all questions and categories
    #  ----------------------------------------------------------------
    def test_get_all_questions_and_categories(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    #  test 404 on GET all questions no results
    #  ----------------------------------------------------------------
    def test_404_get_all_questions_and_categories(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  test DELETE question by question id
    #  ----------------------------------------------------------------
    def test_delete_question_by_question_id(self):
        number = 4
        res = self.client().delete('/questions/' + str(number))
        data = json.loads(res.data)
        question = Question.query.get(number)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    #  test 422 on DELETE question by question id
    #  ----------------------------------------------------------------
    def test_404_delete_question_by_question_id(self):
        number = 0
        res = self.client().delete('/questions/' + str(number))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  test POST new question, not search
    #  ----------------------------------------------------------------
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['new_question'])

    #  test POST questions with search term
    #  ----------------------------------------------------------------
    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'who'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])

    # @TODO: add a test for 422 on POST questions endpoint

    #  test GET questions by category id
    #  ----------------------------------------------------------------
    def test_get_questions_by_category_id(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['total_questions'], 3)

    #  test 404 on GET questions by category
    #  ----------------------------------------------------------------
    def test_404_get_questions_by_category_id(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    #  test POST to play game (/quizzes)
    #  ----------------------------------------------------------------
    def test_play_game(self):
        res = self.client().post('/quizzes', json=self.play_game)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    #  test 404 POST to play game (/quizzes)
    #  ----------------------------------------------------------------
    def test_404_play_game(self):
        res = self.client().post('/quizzes', json=self.play_game_404)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
