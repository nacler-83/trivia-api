#  --------------------------------------------------------------------------#
#  Imports
#  --------------------------------------------------------------------------#


import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

import random

from models import setup_db, Question, Category
from auth.auth import AuthError, requires_auth


#  --------------------------------------------------------------------------#
#  Helpers
#  --------------------------------------------------------------------------#


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    # helper to paginate the questions
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question for question in selection]
    current_selection = questions[start:end]

    return current_selection


def convert_categories(categories):
    # helper to convert categories to a dictionary
    categories_dictionary = {}
    for category in categories:
        categories_dictionary[category.id] = category.type

    return categories_dictionary


#  --------------------------------------------------------------------------#
#  APP Setup & Routes
#  --------------------------------------------------------------------------#


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    #  setup CORS
    #  ----------------------------------------------------------------
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-All-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    #  ROUTE: get all the categories
    #  ----------------------------------------------------------------
    @app.route('/categories', methods=['GET'])
    @requires_auth('get:categories')
    def get_categories(payload):

        try:

            categories = Category.query.all()
            categories_dictionary = convert_categories(categories)

            if (len(categories_dictionary) == 0):
                abort(404)

            result = {
                'success': True,
                'categories': categories_dictionary
            }

            return jsonify(result), 200

        except AuthError:
            abort(401)

        except(Exception):
            abort(422)

    #  ROUTE: post a new question or search questions
    #  ----------------------------------------------------------------
    @app.route('/categories', methods=['POST'])
    @requires_auth('post:categories')
    def create_category(payload):

        try:
            body = request.get_json()
            new_type = body.get('type', None)

            new_category = Category(type=new_type)
            new_category.insert()

            result = {
                'success': True,
                'new_category': new_category.id
            }

            return jsonify(result), 200

        except AuthError:
            abort(401)

        except(Exception):
            abort(422)

    #  ROUTE: get all the questions including pagination handling
    #  ----------------------------------------------------------------
    @app.route('/questions', methods=['GET'])
    @requires_auth('get:questions')
    def get_questions(payload):

        try:

            selection = list(map(Question.format, Question.query.all()))
            current_selection = paginate_questions(request, selection)

            if (len(current_selection) == 0):
                abort(404)

            result = {
                'success': True,
                'questions': current_selection,
                'total_questions': len(selection)
            }

            return jsonify(result), 200

        except AuthError:
            abort(401)

        except(Exception):
            abort(422)

    #  ROUTE: delete a question using question ID
    #  ----------------------------------------------------------------
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    @requires_auth('delete:questions')
    def delete_question(payload, question_id):

        try:
            question = Question.query.get(question_id)

            if question is None:
                abort(404)

            question.delete()

            result = {
                'success': True
            }

            return jsonify(result), 200

        except AuthError:
            abort(401)

        except(Exception):
            abort(422)

    #  ROUTE: post a new question or search questions
    #  ----------------------------------------------------------------
    @app.route('/questions', methods=['POST'])
    @requires_auth('post:questions')
    def create_question(payload):

        try:
            body = request.get_json()
            search = body.get('searchTerm', None)
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            if search:

                selection = list(map(Question.format, Question.query.filter(
                            Question.question.ilike('%{}%'.format(search)))))
                current_selection = paginate_questions(request, selection)
                result = {
                    'success': True,
                    'questions': current_selection,
                    'total_questions': len(selection)
                }

                return jsonify(result)

            else:

                new_question = Question(question=question,
                                        answer=answer,
                                        difficulty=difficulty,
                                        category=category)
                new_question.insert()

                result = {
                    'success': True,
                    'new_question': new_question.id
                }

                return jsonify(result), 200

        except AuthError:
            abort(401)

        except(Exception):
            abort(422)

    #  ROUTE: patch an existing question
    #  ----------------------------------------------------------------
    @app.route('/questions/<int:question_id>', methods=['PATCH'])
    @requires_auth('patch:questions')
    def update_question(payloan, question_id):

        try:
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            current_question = Question.query.filter(Question.id == question_id).one_or_none()

            if not current_question:
                abort(404)

            if question:
                current_question.question = question

            if answer:
                current_question.answer = answer

            if difficulty:
                current_question.difficulty = difficulty

            if category:
                current_question.category = category

            current_question.update()

            result = {
                'success': True,
                'question': current_question.id
            }

            return jsonify(result), 200

        except AuthError:
            abort(401)

        except(Exception):
            abort(422)

    #  ROUTE: get all the questions by category
    #  ----------------------------------------------------------------
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    @requires_auth('get:categories')
    def get_questions_by_category(category_id):

        try:

            selection = list(map(Question.format, Question.query.filter(
                        Question.category == category_id).all()))
            current_selection = paginate_questions(request, selection)

            if (len(selection) == 0):
                abort(404)

            result = {
                'success': True,
                'questions': current_selection,
                'total_questions': len(selection)
            }

            return jsonify(result), 200

        except AuthError:
            abort(401)

        except(Exception):
            abort(422)

    #  ERROR: 404 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    #  ERROR: 422 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    #  ERROR: 400 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    #  ERROR: 405 error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    #  ERROR: Auth error handling
    #  ----------------------------------------------------------------
    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code

    return app
