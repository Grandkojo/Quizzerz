from flask import Flask, session, jsonify
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import timedelta
# from flask_session import Session


# Import and register blueprints
from api.views.user import user_blueprint
from api.v1.users import user_app_views
from api.v1.questions import questions_app_views
from api.v1.results import result_app_views
from api.views.admin import admin_blueprint


load_dotenv()

app = Flask(__name__)

# Configurations
app.secret_key = os.getenv('FLASK_SECRET', str(uuid.uuid4()))
app.config['OAUTH2_META_URL'] = os.getenv('OAUTH2_META_URL')
app.config['OAUTH2_CLIENT_ID'] = os.getenv('OAUTH2_CLIENT_ID')
app.config['OAUTH2_CLIENT_SECRET'] = os.getenv('OAUTH2_CLIENT_SECRET')

# sql_file = os.getenv('SQL_FILE')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=1)
app.debug = True

app.config['CACHE_TYPE'] = 'simple'
# app.config['SESSION_TYPE'] = 'filesystem'  # Optional: Use filesystem to store sessions
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1) 

# cache = Cache(app)
# Session(app)


# Initialize database
db = SQLAlchemy(app)

# Initialize OAuth
oauth = OAuth(app)

# Register OAuth client
Quizzerz = oauth.register(
    name="Quizzerz",
    server_metadata_url=app.config['OAUTH2_META_URL'],
    client_id=app.config['OAUTH2_CLIENT_ID'],
    client_secret=app.config['OAUTH2_CLIENT_SECRET'],
    client_kwargs={"scope": "openid profile email https://www.googleapis.com/auth/user.gender.read"}
)



CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(user_app_views, url_prefix='/api/v1')
app.register_blueprint(questions_app_views, url_prefix='/api/v1')
app.register_blueprint(result_app_views, url_prefix='/api/v1')
app.register_blueprint(admin_blueprint, url_prefix='/admin/')
app.register_blueprint(user_blueprint)


@app.teardown_appcontext
def teardown(error=None):
    """Closes the database session"""
    if error:
        print(f'Teardown error: {error}')
    db.session.remove()

@app.errorhandler(404)
def not_found(error):
    """Returns a JSON error page"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    from app import app
    from api.views.db import *
    with app.app_context():
        db.create_all()
    port = os.getenv('FLASK_PORT', 5000)
    app.run(port=int(port), host='0.0.0.0')
