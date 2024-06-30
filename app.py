from flask import Flask
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
import uuid

load_dotenv()

app = Flask(__name__)

# Configurations
app.secret_key = os.getenv('FLASK_SECRET', str(uuid.uuid4()))
app.config['OAUTH2_META_URL'] = os.getenv('OAUTH2_META_URL')
app.config['OAUTH2_CLIENT_ID'] = os.getenv('OAUTH2_CLIENT_ID')
app.config['OAUTH2_CLIENT_SECRET'] = os.getenv('OAUTH2_CLIENT_SECRET')
sql_file = os.getenv('SQL_FILE')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True

# Initialize OAuth
oauth = OAuth(app)

# Initialize database
db = SQLAlchemy(app)

# Register OAuth client
Quizzerz = oauth.register(
    name="Quizzerz",
    server_metadata_url=app.config['OAUTH2_META_URL'],
    client_id=app.config['OAUTH2_CLIENT_ID'],
    client_secret=app.config['OAUTH2_CLIENT_SECRET'],
    client_kwargs={"scope": "openid profile email https://www.googleapis.com/auth/user.gender.read"}
)


# Import and register blueprints
from api.views.user import user_blueprint
app.register_blueprint(user_blueprint)


if __name__ == "__main__":
    from app import app
    from api.views.db import *
    with app.app_context():
        db.create_all()
    port = os.getenv('FLASK_PORT', 5000)
    app.run(port=int(port), host='0.0.0.0')
