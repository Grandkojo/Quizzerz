from flask import Blueprint, jsonify, abort, request
# from api.v1 import app_views

questions_app_views = Blueprint('questions_app_views', __name__, url_prefix='/api/v1')

@questions_app_views.route('/questions', methods=["GET"], strict_slashes=False)
def get_all_questions():
    """ Retrieves the list of all user objects
    """
    from api.views.db import QuestionDetails
    questions = QuestionDetails.query.all()
    return jsonify([question.to_dict() for question in questions])

@questions_app_views.route('questions/<int:question_id>', methods=["GET"], strict_slashes=False)
def get_question_by_id(question_id):
    """ Retrieves a user object
    """
    from api.views.db import QuestionDetails
    question = QuestionDetails.query.filter_by(questionid=question_id).first()
    if question is None:
        abort(404)
    return jsonify(question.to_dict())

@questions_app_views.route('/answers', methods=["GET"], strict_slashes=False)
def get_all_answers():
    """ Retrieves the list of all answer objects
    """
    from api.views.db import AnswerOptions
    answers = AnswerOptions.query.all()
    return jsonify([answer.to_dict() for answer in answers])

@questions_app_views.route('/answers/<int:question_id>', methods=["GET"], strict_slashes=False)
def get_answer_by_questionid(question_id):
    """ Retrieves the list of all answer objects
    """
    from api.views.db import AnswerOptions
    answers = AnswerOptions.query.filter_by(questionid=question_id).all()

    return jsonify([answer.to_dict() for answer in answers])


@questions_app_views.route('/questions', methods=["POST"], strict_slashes=False)
def add_question():
    """ Add a new question """
    from api.views.db import Categories, QuestionDetails, Questions, AnswerOptions
    from app import db
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "question_text" not in data:
        return jsonify({"error": "Missing question text"}), 400
    if "cat_alias" not in data:
        return jsonify({"error": "Missing category alias"}), 400
    if "answer_options" not in data or not isinstance(data["answer_options"], list):
        return jsonify({"error": "Missing or invalid answer options"}), 400

    cat_alias = data.get("cat_alias")
    category = Categories.query.filter_by(cat_alias=cat_alias).first()    
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    new_question = Questions(question_category=category.category_name)
    db.session.add(new_question)
    db.session.commit()

    question_detail = QuestionDetails(
        questionid=new_question.questionid,
        cat_alias=category.cat_alias,
        question_text=data.get("question_text")
    )
    db.session.add(question_detail)
    db.session.commit()

    for option in data["answer_options"]:
        new_option = AnswerOptions(
            questionid=new_question.questionid,
            answer_text=option.get("answer_text"),
            is_correct=option.get("is_correct", False)
        )
        db.session.add(new_option)
    
    db.session.commit()

    return jsonify({"message": "Question added successfully", "question_id": new_question.questionid}), 201

@questions_app_views.route('/questions/<int:question_id>', methods=["DELETE"], strict_slashes=False)
def delete_question(question_id):
    from api.views.db import Questions, AnswerOptions, QuestionDetails
    from app import db

    question = Questions.query.get(question_id)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    # Delete associated answer options and question details first
    AnswerOptions.query.filter_by(questionid=question_id).delete()
    QuestionDetails.query.filter_by(questionid=question_id).delete()
    db.session.commit()

    # Delete the question itself
    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"}), 200