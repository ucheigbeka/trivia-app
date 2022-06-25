import os
import unittest

from flaskr import create_app
from dotenv import load_dotenv
from models import setup_db, Question, Category


load_dotenv('.env')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.default_categories = ['Science', 'Entertainment', 'Sports']

        self.default_questions = [
            {
                'question': 'What year was the first MCU movie released?',
                'answer': '2008',
                'category': self.default_categories[1],
                'difficulty': 4
            },
            {
                'question': 'Who is the greatest footballer of all time?',
                'answer': 'Lionel Messi',
                'category': self.default_categories[2],
                'difficulty': 1
            },
            {
                'question': 'Who won the Oscars awards for best actor 2022?',
                'answer': 'Will Smith',
                'category': self.default_categories[1],
                'difficulty': 3
            },
            {
                'question': 'What scientist was associated with the Tower of Pisa?',
                'answer': 'Galileo Galilei',
                'category': self.default_categories[0],
                'difficulty': 5
            }
        ]

        self.app = create_app()
        self.client = self.app.test_client()
        self.database_path = os.environ.get('TEST_DATABASE_PATH')
        self.db = setup_db(self.app, self.database_path)

        with self.app.app_context():
            # create all tables
            self.db.create_all()
            # insert default data
            for default_question in self.default_questions:
                default_category = default_question.pop('category')
                question = Question(**default_question)
                category = Category.query.filter_by(type=default_category).first()
                if not category:
                    category = Category(type=default_category)
                question._category = category
                question.insert()
    
    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            Question.query.delete()
            Category.query.delete()
            self.db.session.commit()

    def test_questions_query(self):
        response = self.client.get('/questions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['total_questions'], len(self.default_questions))
        self.assertEqual(len(response.json['categories']), len(self.default_categories))

    def test_questions_query_pagination(self):
        response = self.client.get('/questions', query_string={'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['questions'], [])

    def test_questions_query_by_category(self):
        category = Category.query.filter_by(type='Entertainment').first()
        response = self.client.get(f'/categories/{category.id}/questions')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['total_questions'], len(category.questions))
        for question in response.json['questions']:
            with self.subTest():
                self.assertEqual(question['category'], category.id)

    def test_questions_query_by_category_with_wrong_data(self):
        response = self.client.get('/categories/100/questions')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['success'], False)

    def test_questions_query_with_search_term(self):
        search_term = 'footballer'
        response = self.client.post('/questions', json={'searchTerm': search_term})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['total_questions'], 1)
        for question in response.json['questions']:
            with self.subTest():
                self.assertRegex(question['question'], search_term)

    def test_questions_query_with_wrong_search_term(self):
        search_term = 'cake'
        response = self.client.post('/questions', json={'searchTerm': search_term})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['questions'], [])

    def test_delete_question(self):
        qid = Question.query.filter_by(answer='Will Smith').first().id
        response = self.client.delete(f'/questions/{qid}')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json['success'])
        for question in Question.query.all():
            with self.subTest():
                self.assertNotEqual(question.id, qid)

    def test_delete_wrong_question(self):
        response = self.client.delete('/questions/1000')
        self.assertEqual(response.status_code, 404)

    def test_query_categories(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(sorted(list(response.json['categories'].values())), sorted(self.default_categories))

    def test_add_question(self):
        new_question = {
            'question': 'Who is regarded as the father of modern chemistry?',
            'answer': 'Antoine Lavoisier',
            'difficulty': 4,
            'category': Category.query.filter_by(type='Science').first().id
        }
        response = self.client.post('/questions', json=new_question)
        question = Question.query.filter_by(question=new_question['question']).first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['success'], True)
        self.assertIsNotNone(question)
        for attr in new_question:
            with self.subTest():
                self.assertEqual(getattr(question, attr), new_question[attr])

    def test_add_wrong_question(self):
        new_question = {
            'question': 'What is the name of Naruto\'s father?',
            'answer': 'Minato Namikaze',
            'difficulty': 2,
            'category': -10
        }
        response = self.client.post('/questions', json=new_question)
        self.assertEqual(response.status_code, 404)

    def test_quiz_play_through(self):
        previous_questions = []
        runs = 0
        category = Category.query.filter_by(type=self.default_categories[0]).first()

        while runs < len(category.questions) + 1:
            body = {
                'quiz_category': {'type': category.type, 'id': category.id},
                'previous_questions': previous_questions
            }
            response = self.client.post('/quizzes', json=body)
            if not response.json['question']:
                break
            if response.json['question']['id'] in previous_questions:
                self.fail('Duplicate question')
            previous_questions.append(response.json['question']['id'])
            self.assertEqual(response.status_code, 200)
            runs += 1
        else:
            self.fail('Quiz didn\'t terminate as expected')
        self.assertTrue(True)

    def test_quiz_with_wrong_data(self):
        response = self.client.post('/quizzes', json={'quiz_category': None})
        self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
