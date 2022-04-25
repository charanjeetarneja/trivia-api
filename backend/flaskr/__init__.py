import os
from sre_parse import CATEGORIES
from tkinter.messagebox import QUESTION
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from itsdangerous import NoneAlgorithm

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  #cors = CORS(app, resources={r"*/api/*": {"origins": "*"}})
  cors = CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization,true')
    response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
    return response
  
  # To implement paging of the questions

  def paging_on_questions(request,selection):
    page=request.args.get('page',1,type=int)
    start = (page - 1)*QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions=[question.format() for question in selection]
    return questions[start:end]


  # Route to get all categories
  @app.route('/categories')
  def get_all_categories():
    categories = Category.query.all()
   
    if categories is None:
      abort(404)

    all_cat={}
    for cat in categories:
      all_cat[cat.id]=cat.type

    return jsonify({
      'success': True,
      'categories': all_cat
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  #Route to get all questions in paginated format
  @app.route('/questions')
  def get_all_questions():
    all_questions=Question.query.order_by(Question.id).all()
    page_of_questions=paging_on_questions(request,all_questions)
    
    #Abort if page doesn't exists
    if len(page_of_questions) == 0:
      abort(404)
    
    all_categories=Category.query.all()
    all_cat={}
    for cat in all_categories:
      all_cat[cat.id]=cat.type

    return jsonify({
      'success' : True,
      'questions': page_of_questions,
      'totalQuestions' : len(all_questions),
      'categories' : all_cat
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

  # Route to get question based on a category id
  @app.route('/categories/<int:cat_id>/questions')
  def get_questions(cat_id):
    
    category=Category.query.filter_by(id=cat_id).one_or_none()
    
    if category is None:
      abort(404)
    
    questions_in_category=Question.query.filter_by(category=str(cat_id)).all()
    page_of_questions=paging_on_questions(request,questions_in_category)
    
    return(jsonify({
      'success':True,
      'questions': page_of_questions,
      'totalQuestions': len(questions_in_category),
      'currentCategory': category.type
    }))
  
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  #Route to delete a question using id
  @app.route('/questions/<int:id>',methods=['DELETE'])
  def delete_questions(id):
    
    question_to_delete=Question.query.filter_by(id=id).one_or_none()

    if question_to_delete is None:
      abort(404)
    
    question_to_delete.delete()

    return jsonify({
      'success':True
    })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  #Route to add a question
  @app.route('/questions',methods=['POST'])
  def add_question():
    
    req_body=request.get_json()
    print(req_body)
    
    ques=req_body.get('question',None)
    ans=req_body.get('answer',None)
    diff=req_body.get('difficulty',None)
    cat=req_body.get('category',None)
    
    try:
      question=Question(question=ques, answer=ans, difficulty=diff, category=cat)
      question.insert()

    except Exception as e:
      print(e)
      abort(422)
    
    return jsonify({
      'success':True
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  #Route to return questions based on search term
  @app.route('/search', methods=['POST'])
  def search_questions():
    
    req_body=request.get_json()
    search=req_body.get('searchTerm',None)
    search_output=Question.query.filter(Question.question.ilike('%'+search+'%')).all()
    
    if search_output is None:
      abort(404)
    page_of_questions=paging_on_questions(request,search_output)
    
    #Abort if page doesn't exists
    if len(page_of_questions) == 0:
      abort(404)

    return jsonify({
      'success':True,
      'questions':page_of_questions,
      'total_questions':len(search_output)
  })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  #POST endpoint to get questions to play the quiz.
  @app.route('/quizzes', methods=['POST'])
  def questions_for_quiz():
    req_body=request.get_json()
    if (req_body is None ):
          all_questions = Question.query.all()
          quiz_cat['id']=0  
          prev_ques=[]
    else:
      quiz_cat=req_body.get('quiz_category')
      prev_ques=req_body.get('previous_questions')

    try:
      if (quiz_cat['id'] == 0 ):
          all_questions = Question.query.all()
      else:
          all_questions = Question.query.filter_by(category=quiz_cat['id']).all()
    
      ran_index = random.randint(0, len(all_questions)-1)
      next_ques = all_questions[ran_index]

      while next_ques.id not in prev_ques:
          next_ques = all_questions[ran_index]
          return jsonify({
            'success': True,
            'question': next_ques.format(),
            'previousQuestion': prev_ques
            })
    except Exception as e:
      print(e)
      abort(404)

  #Error handlers

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      'error': 400,
      "message": "Bad request"
    }), 400

  @app.errorhandler(404)
  def page_not_found(error):
      return jsonify({
        "success": False,
        'error': 404,
        "message": "Page not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable_recource(error):
      return jsonify({
        "success": False,
        'error': 422,
        "message": "Unprocessable resource"
      }), 422


  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
        "success": False,
        'error': 500,
        "message": "Internal server error"
      }), 500

  @app.errorhandler(405)
  def invalid_method(error):
      return jsonify({
        "success": False,
        'error': 405,
        "message": "Invalid method!"
      }), 405
      
  return app

    