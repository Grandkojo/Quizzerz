from flask import Blueprint, jsonify, request, redirect, session, url_for, render_template, flash
import requests
import json
from authlib.integrations.flask_client import OAuth
from datetime import datetime

user_blueprint = Blueprint('user_bp', __name__, template_folder='templates')

@user_blueprint.route('/')
def index():
    return render_template('index.html')

@user_blueprint.route('/home')
def home():
    method = request.args.get('method')
    user_data = session.get('user')
    print("Session retrieved on /home:", user_data)
    # return jsonify({"user_data": user_data})
    if user_data:
        if method == "google" or method == "quizzerz":
            return render_template('home.html', user_data=user_data, method=method)
    else:
        return redirect(url_for("user_bp.index"))
    return render_template('home.html', user_data=user_data, method=method)

@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    from api.views.db import Users
    from app import db
    error = None
    if request.method == 'POST':
        form_data = request.form
        email = form_data.get('user_email')
        password = form_data.get('user_password')
        username = form_data.get('user_name')

        if not email or not password or not username:
            error = "All fields are required."
            return render_template('signup.html', error=error)

        # Check if the email or username already exists
        existing_user = Users.query.filter((Users.email == email) | (Users.username == username)).first()
        
        if existing_user:
            if existing_user.email == email:
                error = "Email already exists, login instead"
            elif existing_user.username == username:
                error = "Username already exists, try another"
        else:
            new_user = Users(username=username, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            session.permanent = True
            session['user'] = {"user_id":new_user.userid, "email": email, "username": username}
            print(session['user'])
            return redirect(url_for('user_bp.signup_complete'))
        
        return render_template('signup.html', error=error)
    
    elif request.method == "GET":
        user = session.get("user")

        if user is None:
            return render_template('signup.html')
        
        else:
            return redirect(url_for('user_bp.signup_complete'))
            # print("Session retrieved on GET request:", user)
            # return jsonify({"user": user})
    
    return render_template('signup.html')
    

@user_blueprint.route('/signup-complete')
def signup_complete():
    user_data = session.get('user')
    if user_data:
        return redirect(url_for('user_bp.home', method="quizzerz"))
    return redirect(url_for('user_bp.signup'))

@user_blueprint.route('/login')
def login():
    return render_template('login.html')

@user_blueprint.route("/quizzerz-login", methods=["POST", "GET"])
def quizzerz_login():
    from api.views.db import Users
    error = None
    if request.method == "POST":
        form_data = request.form
        email = form_data.get("user_email")
        password = form_data.get("user_password")

        if not email or not password:
            error = "Email and password are required."
            return render_template("login.html", error=error)

        user = Users.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.permanent = True
            session['user'] = {"user_id":user.userid, "email": email, "username": user.username}
            # return jsonify({"user": session['user']})
            flash("You were successfully logged in")
            return redirect(url_for('user_bp.home', method="quizzerz"))
        else:
            error = "Invalid email or password"
    
    return render_template("login.html", error=error)

@user_blueprint.route("/google-login")
def google_login():
    from app import oauth  # Import here to avoid circular import
    redirect_uri = url_for("user_bp.authorize", _external=True)
    return oauth.Quizzerz.authorize_redirect(redirect_uri)

@user_blueprint.route("/authorize")
def authorize():
    from app import oauth  # avoid circular import
    token = oauth.Quizzerz.authorize_access_token()
    personal_data_url = "https://people.googleapis.com/v1/people/me?personFields=genders"
    
    gender = requests.get(
        personal_data_url,
        headers={"Authorization": f"Bearer {token['access_token']}"}).json()
    
    token['gender'] = gender
    session['user'] = token

    return redirect(url_for("user_bp.home", method="google"))

@user_blueprint.route("/quiz/<string:sect>")
def quiz(sect):
    from api.views.db import QuestionDetails, AnswerOptions
    sections = ['mat', 'sci', 'geo', 'eng']

    if session.get("user"):
        if sect in sections:
            questions = QuestionDetails.query.filter_by(cat_alias=sect).all()
            question_ids = [q.questionid for q in questions]
            options = AnswerOptions.query.filter(AnswerOptions.questionid.in_(question_ids)).all()
            # is_correct = [c.is_correct for c in options]

            combined = []
            for question in questions:
                question_options = []
                for opt in options:
                    if opt.questionid == question.questionid:
                        option_data = {
                            "answer_text": opt.answer_text,
                            "is_correct": opt.is_correct
                        }
                        question_options.append(option_data)
                
                combined.append({
                    "question_text": question.question_text,
                    "options": question_options
                })
            
            session.permanent = True
            session["quiz_details"] = combined

            return render_template("questions.html", questions=combined, sect=sect)
        

        return jsonify({"error": "Invalid section"}), 400
    error="Login to access questions"
    return render_template("login.html",error=error)

@user_blueprint.route('/calculate_score', methods=['POST'])
def calculate_score():
    from api.views.db import QuestionDetails, AnswerOptions
    data = request.get_json()
    selected_answers = data['selected_answers']
    selected_answers = [ans for ans in selected_answers if ans is not None]

    sect = data['sect']

    questions = QuestionDetails.query.filter_by(cat_alias=sect).all()
    question_ids = [q.questionid for q in questions]
    answer_solution = AnswerOptions.query.with_entities(AnswerOptions.answerid, AnswerOptions.is_correct).filter(AnswerOptions.answer_text.in_(selected_answers)).all()
    # answer_id = AnswerOptions.query.with_entities(AnswerOptions.answerid, AnswerOptions.answer_text, AnswerOptions.is_correct).filter(AnswerOptions.questionid.in_(question_ids)).all()
    # options = AnswerOptions.query.filter(AnswerOptions.questionid.in_(question_ids)).all()
    # correct_answers = AnswerOptions.query.with_entities(AnswerOptions.answer_text, AnswerOptions.is_correct).filter(AnswerOptions.answer_text.in_(selected_answers)).all()


    print(selected_answers)
    print(answer_solution)
    print(question_ids)
    for answerid, is_correct in answer_solution:
        print(f"Answer: {answerid}, Is Correct: {is_correct}")
   
    score = sum(1 for _, answer in answer_solution if answer == True)
    total_questions = len(question_ids)


    print(f"{score} out of {total_questions}")

    selected_answers_with_correctness = [
    {"answer_text": answer, "is_correct": is_correct} 
    for answer, (answerid, is_correct) in zip(selected_answers, answer_solution)
    ]

    session.permanent = True

    if session.get("user"):
        user_id = session['user'].get('user_id')
    else:   
        return "No user"

    if 'quiz_details' not in session:
        # session['quiz_details'] = []
        return "No quiz session"
    
    quiz_details = session['quiz_details']
    quiz_details.append({
        "user_id": user_id,
        "selected_answers": selected_answers_with_correctness,
        "score": score,
        "length": total_questions,
        "section": sect
    })

    session['quiz_details'] = quiz_details
    session['results_processed'] = False

    return redirect(url_for('user_bp.results',score=score))

@user_blueprint.route('/results', methods=["GET"])
def results():
    from api.views.db import QuizResults
    from app import db

    score = request.args.get('score', 0)
    quiz_details = session.get('quiz_details', [])

    user_id = quiz_details[-1].get("user_id")
    category = quiz_details[-1].get("section")
    quiz_score = quiz_details[-1].get("score") 
    # if user_id and category and quiz_score:

    # existing_result = QuizResults.query.filter_by(userid=user_id, catalias=category).first()
    # if not existing_result:
    if not session.get('results_processed'):
        results = QuizResults(userid=user_id, catalias=category, result=quiz_score, details=quiz_details, timestamp=datetime.now())
        db.session.add(results)
        db.session.commit()
        session['results_processed'] = True
    # else:
        # return "Same"
    
    return render_template('results.html', score=score, quiz_details=quiz_details)
    # else:
        # return "Incorrect parameters"
    
    # return jsonify({"quiz_details": quiz_detailss})
    return jsonify({"user_id": user_id, "category": category, "quiz_score": quiz_score})


@user_blueprint.route('/results-history', methods=["GET"])
def results_history():
    from api.views.db import QuizResults

    if session.get("user"):
        user_id = session['user'].get('user_id')
    else:
        return "No user logged in", 403
    
    # quiz_details = session.get('quiz_details', [])

    # category = request.args.get('category')
    # if not category:
    #     return "Category not specified."

    history = QuizResults.query.filter_by(userid=user_id).order_by(QuizResults.timestamp.desc()).all()
    return render_template("results_history.html", history=history)

@user_blueprint.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("user_bp.index"))
