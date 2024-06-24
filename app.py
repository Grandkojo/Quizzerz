from flask import Flask, url_for, jsonify, render_template, redirect, session, request
import requests
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
import os
import json
import uuid

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('FLASK_SECRET', str(uuid.uuid4()))

# Initialize OAuth
oauth = OAuth(app)

Quizzerz = oauth.register(
    name="Quizzerz",
    server_metadata_url=os.getenv('OAUTH2_META_URL'),
    client_id=os.getenv('OAUTH2_CLIENT_ID'),
    client_secret=os.getenv('OAUTH2_CLIENT_SECRET'),
    client_kwargs={"scope": "openid profile email https://www.googleapis.com/auth/user.gender.read"}
)

@app.route('/')
def index():
    
    return render_template('index.html')

@app.route('/home')
def home():
    method = request.args.get('method')
    user_data = session.get('user')
    if user_data:
        if method == "google":
            return render_template('home.html', user_data=user_data, method=method)
        elif method == "quizzerz":
            return render_template('home.html', user_data=user_data, method=method)
    else:
        return url_for("index")

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        form_data = request.form

        user_data = {
            'email': form_data['user_email'],
            'password': form_data['user_password'],
            'user_name': form_data['user_name']
        }
        session['user'] = user_data
        return redirect(url_for('signup_complete'))
    return render_template('signup.html', session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))

@app.route('/signup-complete')
def signup_complete():
    user_data = session.get('user')
    if user_data:
        return redirect(url_for('home', method="quizzerz"))
    return redirect(url_for('signup'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/quizzerz-login")
def quizzerz_login():
    # Do checks later
    checked_user_data = "Yes"
    return redirect(url_for('home', verified=checked_user_data))

@app.route("/google-login")
def google_login():
    redirect_uri = url_for("authorize", _external=True)
    return oauth.Quizzerz.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    token = oauth.Quizzerz.authorize_access_token()
    personal_data_url = "https://people.googleapis.com/v1/people/me?personFields=genders"
    
    gender = requests.get(
        personal_data_url,
        headers={"Authorization": f"Bearer {token['access_token']}"}).json()
    
    token['gender'] = gender
    session['user'] = token

    return redirect(url_for("home", method="google"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = os.getenv('FLASK_PORT', 5000)
    app.run(port=int(port), debug=True)
