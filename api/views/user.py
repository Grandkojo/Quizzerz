from flask import Blueprint, jsonify, request, redirect, session, url_for, render_template, flash
import requests
import json
from authlib.integrations.flask_client import OAuth

user_blueprint = Blueprint('user_bp', __name__, template_folder='templates')

@user_blueprint.route('/')
def index():
    return render_template('index.html')

@user_blueprint.route('/home')
def home():
    method = request.args.get('method')
    user_data = session.get('user')
    if user_data:
        if method == "google" or method == "quizzerz":
            return render_template('home.html', user_data=user_data, method=method)
    else:
        return redirect(url_for("user_bp.index"))

@user_blueprint.route('/signup', methods=['GET', 'POST'])
def signup():
    from api.views.db import Users
    from app import db
    error = None
    if request.method == 'POST':
        form_data = request.form
        user_data = {
            'email': form_data['user_email'],
            'password': form_data['user_password'],
            'user_name': form_data['user_name']
        }
        email = Users.query.with_entities(Users.email).filter_by(email=user_data.get("email")).scalar()

        user_name = Users.query.with_entities(Users.username).filter_by(username=user_data.get("username")).scalar()
        if email == user_data.get("email"):
            error = "Email already exists, login instead"
        elif user_name == user_data.get("user_name"):
            error = "Username already exists, try another"
        else:
            new_user = Users(username=user_data.get("user_name"), email=user_data.get("email"))
            new_user.set_password(user_data.get("password"))
            db.session.add(new_user)
            db.session.commit()
            
            session['user'] = user_data
            return redirect(url_for('user_bp.signup_complete'))
        return render_template('signup.html', error=error)
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
        user_data = {
            "email": form_data["user_email"],
            "password": form_data["user_password"]
        }
        user = Users.query.filter_by(email=user_data.get("email")).first()
        if user and user.check_password(user_data.get("password")):
            session['user'] = user_data
            flash("You were succesfully logged in")
            return redirect(url_for('user_bp.home', method="quizzerz"))
        else:
             error = "Invalid email or password"
        return render_template("login.html", error=error)
    return render_template("login.html")

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

@user_blueprint.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("user_bp.index"))
