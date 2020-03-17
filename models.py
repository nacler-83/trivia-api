# ---------------------------------------------------------------------------#
# Imports
# ---------------------------------------------------------------------------#


import os
import json
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# ---------------------------------------------------------------------------#
# Config
# ---------------------------------------------------------------------------#


database_path = os.environ['DATABASE_URL']
# uncomment the below name and patch for local development
# database_name = "trivia"
# database_path = "postgresql://{}/{}". format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
        binds a flask application and a SQLAlchemy service.
        initialize the app
        create the tables
        setup flask migrate
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)


# ---------------------------------------------------------------------------#
# Models
# ---------------------------------------------------------------------------#


class Question(db.Model):
    '''
    Question
        question = text of the question
        answer = the question's answer
        category = integer aligned to category id
        difficulty = integer 1 - 5, 5 being most difficult
    '''
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
          'id': self.id,
          'question': self.question,
          'answer': self.answer,
          'category': self.category,
          'difficulty': self.difficulty
        }


class Category(db.Model):
    '''
    Category
        id = unique identifier
        type = string name of category
    '''
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
