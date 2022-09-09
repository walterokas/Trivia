from email.mime import base
import os, sys, json
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
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def add_cors(resp):
        #Ensure all responses have the CORS headers. This ensures any failures are also accessible by the client.
        
        resp.headers.add('Access-Control-Allow-Origin', '*')
        resp.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        resp.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')

        #set low for debugging
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
        print(categories)
        catDict = {}
        count = 0
        for category in categories:
            catDict[count] = format(category.type)
            count += 1
    
        #{format(category) for category in categories}
        # return json.dumps(catDict)
        return jsonify(catDict)


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    """
    @app.route('/questions', methods=['GET'])
    def listQuestions():
        page = request.args.get('page', 1 , type=int)
        start = (page-1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        
        questions = Question.query.all()

        formatted_questions = [question.format() for question in questions]

        formatted_categories = {}
        for category in Category.query.all():
            formatted_categories[category.id] = category.type

        result = {
            "questions": formatted_questions[start:end],
            "total_questions": len(questions),
            # "categories": list({category.type for category in Category.query.all()}), #set comprehension cast to list
            "categories": formatted_categories,
            "current_category": []
        }

        # return json.dumps(result)
        return jsonify(result)


    """
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def deleteQuestion(id):
        del_obj = Question.query.filter_by(id=id).first()
        Question.delete(del_obj)

        return jsonify({"status": "Success", "error": "200"})


    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

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

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

