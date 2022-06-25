from random import choice

from flask import Flask, request, abort, Response
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(page, questions):
    start = (page - 1) * QUESTIONS_PER_PAGE
    return questions[start: start + QUESTIONS_PER_PAGE]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def update_headers(response: Response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        categories = dict(Category.query.with_entities(Category.id, Category.type).all())
        return {
                   'categories': categories
               }, 200

    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        questions = [question.format() for question in Question.query.all()]
        paginated_questions = paginate_questions(page, questions)
        categories = dict(Category.query.with_entities(Category.id, Category.type).all())
        return {
            'questions': paginated_questions,
            'total_questions': len(questions),
            'categories': categories,
            'current_category': None
        }, 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get_or_404(question_id)
        question.delete()
        return {
                   'success': True
               }, 200

    @app.route('/questions', methods=['POST'])
    def update_questions():
        page = request.args.get('page', 1, type=int)
        if 'searchTerm' in request.json:
            search_term = f'%{request.json["searchTerm"]}%'
            questions = []
            for question in Question.query.filter(Question.question.ilike(search_term)).all():
                questions.append(question.format())
            paginated_questions = paginate_questions(page, questions)
            return {
                       'questions': paginated_questions,
                       'total_questions': len(questions),
                       'current_category': None
                   }, 200
        else:
            data = request.get_json()
            category_id = data.pop('category')
            question = Question(**data)
            question._category = Category.query.get_or_404(category_id)
            question.insert()
            return {
                'success': True
            }

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        page = request.args.get('page', 1, type=int)
        category = Category.query.get_or_404(category_id)
        questions = [question.format() for question in category.questions]
        paginated_questions = paginate_questions(page, questions)
        return {
            'questions': paginated_questions,
            'total_questions': len(questions),
            'current_category': category.id
        }, 200

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        json = request.get_json()
        default_category = {'type': 'click', 'id': 0}
        if 'previous_questions' not in json or 'quiz_category' not in json:
            abort(422)
        category = json.get('quiz_category', default_category)
        questions_query = Question.query.filter(Question.id.not_in(json.get('previous_questions', [])))
        if category == default_category:
            questions = [question.format() for question in questions_query.all()]
        else:
            questions = [question.format() for question in questions_query.filter_by(category=category['id']).all()]

        next_question = choice(questions) if questions else None

        return {
            'question': next_question
        }

    @app.errorhandler(400)
    def bad_request_error(error):
        return {
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }, 400

    @app.errorhandler(404)
    def not_found_error(error):
        return {
                   'success': False,
                   'error': 404,
                   'message': 'Resource not found'
               }, 404

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        return {
                   'success': False,
                   'error': 405,
                   'message': 'Method not allowed'
               }, 405

    @app.errorhandler(422)
    def unprocessed_entity_error(error):
        return {
                   'success': False,
                   'error': 422,
                   'message': 'Something went wrong'
               }, 422

    return app
