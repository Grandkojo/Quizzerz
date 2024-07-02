from flask import Blueprint, jsonify, request, redirect, session, url_for, render_template, flash
import requests
import json

admin_blueprint = Blueprint('admin_bp', __name__, template_folder='templates/admin', static_folder='/static')


@admin_blueprint.route('/', methods=["GET"])
def admin_index():
    return render_template('admin_index.html')

@admin_blueprint.route('/login', methods=["POST", "GET"])
def login():
    from api.views.db import Admin
    error = None
    if request.method == 'POST':
        form_data = request.form
        email = form_data.get('admin_email')
        password = form_data.get('admin_password')

        if not email or not password:
            error = "Email and password are required."
            return render_template("admin_index.html", error=error)
        
        admin_user = Admin.query.filter_by(admin_email=email).first()
        if admin_user and admin_user.check_password(password):
            session.permanent = True
            session['admin_user'] = {"admin_user_id":admin_user.adminid, "email": email, "name": admin_user.admin_name}

            return redirect(url_for('admin_bp.home'))
        else:
            error = "Invalid email or password"
    
    return render_template("admin_index.html", error=error)

@admin_blueprint.route('/home', methods=["GET"])
def home():
    if not session.get("admin_user"):
        return redirect(url_for("admin_bp.login"))
    return render_template('admin_home.html')

@admin_blueprint.route('/dashboard', methods=["GET"])
def dashboard():
    from api.views.db import QuizResults, Users, QuestionDetails

    quiz_results_count = QuizResults.query.count()
    users_count = Users.query.count()
    question_details_count = QuestionDetails.query.count()

    return render_template('dashboard.html', quiz_count=quiz_results_count, users_count=users_count, questions_count=question_details_count)

@admin_blueprint.route('/users', methods=["GET"])
def users():
    from api.views.db import Users

    users = Users.query.all()

    return render_template('users.html', users=users)

@admin_blueprint.route('/results', methods=["GET"])
def results():
    from api.views.db import QuizResults

    quiz_results = QuizResults.query.all()

    return render_template('results.html', results=quiz_results)



@admin_blueprint.route('/questions', methods=["GET"])
def questions():
    from api.views.db import QuestionDetails, AnswerOptions

    answers = AnswerOptions.query.all()
    questions = QuestionDetails.query.all()

    return render_template('question.html', questions=questions, answers=answers)

@admin_blueprint.route('/profile', methods=["GET"])
def profile():
    from api.views.db import Admin

    if session.get("admin_user"):
        admin_id = session["admin_user"].get("admin_user_id")
        admin = Admin.query.filter_by(adminid=admin_id).first()
        return render_template("profile.html", admin_detail= admin)
    return redirect(url_for("admin_bp.login"))

@admin_blueprint.route('/logout', methods=["GET"])
def logout():
    session.pop("admin_user", None)
    return redirect(url_for("admin_bp.admin_index"))
