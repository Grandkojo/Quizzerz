from flask import Flask, url_for, jsonify, render_template
# from flask_bcrypt import Bcrypt
# from flask_oauthlib.client import OAuth
# from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=5000, debug=True)