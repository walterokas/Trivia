from email.mime import base
import os
import sys
import json
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

# Define path of the parent folder containing the models
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    print("App Created Successful")

    """
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def add_cors(resp):
        # Ensure all responses have the CORS headers.
        # This ensures any failures are also accessible by the client.
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization'
            )
        resp.headers.add(
            'Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE'
            )

        # Set low for debugging
        if app.debug:
            resp.headers['Acess-Control-Max-Age'] = '1'
        return resp

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def listCategories():

        categories = Category.query.all()

        if categories is None:
            abort(404)
            
        formatted_categories = [category.type for category in categories]

        result = {
            "categories": formatted_categories
        }
        return jsonify(result)

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """

    @app.route('/questions', methods=['GET'])
    def listQuestions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]
        formatted_categories = {}

        try:
            for category in Category.query.all():
                formatted_categories[category.id] = category.type
        except:
            abort(404)

        result = {
            "questions": formatted_questions[start:end],
            "total_questions": len(questions),
            "categories": formatted_categories,
            "current_category": []
        }

        # return json.dumps(result)
        return jsonify(result)

    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the
    screen for three pages. Clicking on the page numbers should
    update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def deleteQuestion(id):
        del_obj = Question.query.filter_by(id=id).first()

        try:
            Question.delete(del_obj)
        except:
            abort(404)

        return jsonify({"status": "Success", "error": "200", "id": id})

    """
    TEST: When you click the trash icon next to a question, the question
    will be removed. This removal will persist in the database and when
    you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    """

    @app.route('/questions/add', methods=['POST'])
    def create_Question():
        if request.method == 'POST':
            data = json.loads(request.data)

            # print("NEW CATEGORY ID: ", int(data.get('category', None)) + 1)
            try:
                question_obj = Question(
                    question=data.get('question', None),
                    answer=data.get('answer', None),
                    category=str(int(data.get('category', None)) + 1),
                    difficulty=data.get('difficulty', None)
                    )

                Question.insert(question_obj)

            except:
                abort(422)

        return jsonify({"status": "Question Added Successfully"})

    """
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end
    of the last page of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    """

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        data = json.loads(request.data)
        searchTerm = data.get('searchTerm')

        if searchTerm == "":
            abort(404)

        try:
            questions = Question.query.filter(
                Question.question.ilike("%{}%".format(searchTerm))
                )
        except:
            abort(404)

        formatted_questions = [question.format() for question in questions]

        result = {
            "questions": formatted_questions[start:end],
            "total_questions": questions.count(),
            "current_category": []
        }

        return jsonify(result)

    """
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.
    """

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def getQuestionsByCategory(id):
        page = request.args.get('page', 1, type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.filter_by(category=str(id))
        if questions.count()==0:
            abort(500)
        formatted_questions = [question.format() for question in questions]

        result = {
            "questions": formatted_questions[start:end],
            "total_questions": questions.count(),
            "current_category": []
        }

        return jsonify(result)

    """
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        if request.method != 'POST':
            abort(405)
        if request.method == 'POST':
            data = json.loads(request.data)

            try:
                prevQuestions = data['previous_questions']
            except:
                abort(500)

            category_type = data['quiz_category'].get('type', None)

            matched_category = Category.query.filter_by(
                type=category_type
                ).first()

            try:
                # When a category is selected on the play tab and id is passed
                questions = Question.query.filter_by(
                    category=str(matched_category.id)
                    ).all()
            except:
                # When ALL is selected and no id is passed
                questions = Question.query.all()
            formatted_questions = [
                question.format() for question in questions
                if question.id not in prevQuestions]
            random.shuffle(formatted_questions)

            try:
                question = formatted_questions[0]
            except:
                # abort(404)
                question = None

        result = {
            "question": question,
            }

        return jsonify(result)

    """
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(401)
    def unauthorized(e):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Unauthorized"
        }), 401

    @app.errorhandler(403)
    def forbidden(e):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(e):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500

    @app.errorhandler(501)
    def notImplemented(e):
        return jsonify({
            "success": False,
            "error": 501,
            "message": "Not Implemented"
        }), 501

    @app.errorhandler(502)
    def badGateway(e):
        return jsonify({
            "success": False,
            "error": 502,
            "message": "Bad Gateway"
        }), 502

    @app.errorhandler(503)
    def serviceUnavailable(e):
        return jsonify({
            "success": False,
            "error": 503,
            "message": "Service Unavailable"
        }), 503

    @app.errorhandler(504)
    def gatewayTimeout(e):
        return jsonify({
            "success": False,
            "error": 504,
            "message": "Gateway Timeout"
        }), 504

    @app.errorhandler(505)
    def httpUnsupported(e):
        return jsonify({
            "success": False,
            "error": 505,
            "message": "HTTP Version Not Supported"
        }), 505

    return app