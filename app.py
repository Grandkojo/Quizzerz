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
def home():
    return render_template('home.html', session=session.get("user"), pretty=json.dumps(session.get("user"), indent=4))

@app.route("/google-login")
def google_login():
    redirect_uri = url_for("authorize", _external=True)
    Quizzerz = oauth.create_client('Quizzerz')
    return Quizzerz.authorize_redirect(redirect_uri)

@app.route("/authorize")
def authorize():
    Quizzerz = oauth.create_client('Quizzerz')
    token = Quizzerz.authorize_access_token()
    personal_data_url = "https://people.googleapis.com/v1/people/me?personFields=genders"
    
    gender = requests.get(
        personal_data_url,
        headers={"Authorization": f"Bearer {token['access_token']}"}).json()
    
    token['gender'] = gender
    session['user'] = token
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    port = os.getenv('FLASK_PORT', 5000)
    app.run(port=int(port), debug=True)
