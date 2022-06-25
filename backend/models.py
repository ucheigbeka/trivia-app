import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv('.env')

database_path = os.environ.get('DATABASE_PATH')

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

    return db


# ----------------------------------------------------------------------------#
# Question
# ----------------------------------------------------------------------------#


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String)
    answer = db.Column(db.String)
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    difficulty = db.Column(db.Integer)

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


# ----------------------------------------------------------------------------#
# Category
# ----------------------------------------------------------------------------#


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    questions = db.relationship('Question', backref='_category', lazy=True, cascade='all, delete')

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
