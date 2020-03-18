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
#  Test Configutation
#  --------------------------------------------------------------------------#

'''
Set an auth token to use for the tests. If the token is for an admin
role, set admin = True. If the token is for a user role, set admin = False.
'''
token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlF6WXpSVUkxUWtFeU9FWkZPREZHT1VZeVJFVTBPVFZGTkRaQk9UQkNSRVkyUVVVd01EWTVNUSJ9.eyJpc3MiOiJodHRwczovL25hY2xlci5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWU3MTY2YzEyNjFiZjQwY2FkNTc5ODdlIiwiYXVkIjoidHJpdmlhLWFwaSIsImlhdCI6MTU4NDQ5MzAxMywiZXhwIjoxNTg0NTAwMjEzLCJhenAiOiJiblBubTZOSGJKR2c4bVpsS21nNjR5azN3VzNkMEhXMSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnF1ZXN0aW9ucyIsImdldDpjYXRlZ29yaWVzIiwiZ2V0OnF1ZXN0aW9ucyIsInBhdGNoOnF1ZXN0aW9ucyIsInBvc3Q6Y2F0ZWdvcmllcyIsInBvc3Q6cXVlc3Rpb25zIl19.oij13phRMlr23DMeUMZYTZI9HCaEBOn6oSsjlIuXaTG5qcYG6-uUbnes9MtaTcPkZPU-CQkmKepmmhYlaurGdQDGoRR7VI9lprUn36eV77tq8TcW5GcD_TTEo5w5-IFz-QmH2znHv4K4qFfOYyp9Y_orjAwnJoH18vNHTOsGjytp8nPzo3FCXQcAj2mWmQw1v9DQJQ9B7WV1giqBAd4ORnSgU_lDIhivsBV43rtJHbGdZGBCULyzY_sxM39lKblriEO_Vh9iXt_qw4lzRjIKMycIRqC5YAmL_PE4PrieHE62NRrg_3p_FCELNGBKVoQmm87mzWzoQdrK3kVwG9CFvQ'
admin = True


#  --------------------------------------------------------------------------#
#  Classes and Tests
#  --------------------------------------------------------------------------#


class TriviaTestCase(unittest.TestCase):
    '''
    This class represents the trivia test case
    '''
    def setUp(self):
        # Defines test variables and initializes app
        self.app = create_app()
        self.client = self.app.test_client
        # Defines a jwt to use in the tests
        self.headers = {"Content-Type'": "application/json", "Authorization": f"Bearer {token}"}
        # Sets up the database
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
        res = self.client().get('/categories', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    #  test GET all questions
    #  ----------------------------------------------------------------
    def test_get_all_questions(self):
        res = self.client().get('/questions', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))

    if admin == True:

        #  test 404 on GET all questions no results
        #  ----------------------------------------------------------------
        def test_404_get_all_questions(self):
            res = self.client().get('/questions?page=1000', headers=self.headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')

        #  test DELETE question by question id
        #  ----------------------------------------------------------------
        def test_delete_question_by_question_id(self):
            number = 4
            res = self.client().delete('/questions/' + str(number), headers=self.headers)
            data = json.loads(res.data)
            question = Question.query.get(number)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(question, None)

        #  test 404 on DELETE question by question id
        #  ----------------------------------------------------------------
        def test_404_delete_question_by_question_id(self):
            number = 1000
            res = self.client().delete('/questions/' + str(number), headers=self.headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')

        #  test POST new question, not search
        #  ----------------------------------------------------------------
        def test_create_new_question(self):
            res = self.client().post('/questions', json=self.new_question, headers=self.headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['new_question'])

        #  test POST questions with search term
        #  ----------------------------------------------------------------
        def test_search_questions(self):
            res = self.client().post('/questions', json={'searchTerm': 'who'}, headers=self.headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['total_questions'])
            self.assertTrue(data['questions'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
