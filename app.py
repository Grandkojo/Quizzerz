from flask import Flask
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
import os
import uuid

load_dotenv()

app = Flask(__name__)

# Configurations
app.secret_key = os.getenv('FLASK_SECRET')
app.config['OAUTH2_META_URL'] = os.getenv('OAUTH2_META_URL')
app.config['OAUTH2_CLIENT_ID'] = os.getenv('OAUTH2_CLIENT_ID')
app.config['OAUTH2_CLIENT_SECRET'] = os.getenv('OAUTH2_CLIENT_SECRET')

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

# Import and register blueprints
from api.views.user import user_blueprint
app.register_blueprint(user_blueprint)

if __name__ == "__main__":
    port = os.getenv('FLASK_PORT', 5000)
    app.run(port=int(port), debug=True)
