from flask import Blueprint, jsonify, abort, request

# from api.v1 import app_views

user_app_views = Blueprint('user_app_views', __name__, url_prefix='/api/v1')

@user_app_views.route('/users', methods=["GET"], strict_slashes=False)
def get_all_users():
    """ Retrieves the list of all user objects
    """
    from api.views.db import Users
    users = Users.query.all()
    return jsonify([user.to_dict() for user in users])

@user_app_views.route('/users/<int:user_id>', methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """ Retrieves a user object
    """
    from api.views.db import Users
    user = Users.query.filter_by(userid=user_id).first()
    if user is None:
        abort(404)
    return jsonify(user.to_dict())

""" this api creates a new user into the database
    it's a post request that requires data
    data: the json data
    data["email"]: the email of the new user
    data["password"]: the password of the user that will be hashed before
    entry into the database
    data["username"]: the username the user prefere
"""
@user_app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """ Creates a new user into the database
    """
    from api.views.db import Users
    from app import db
    from sqlalchemy.exc import IntegrityError

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    if "username" not in data:
        return jsonify({"error": "Missing username"}), 400
    
    try:
        new_user = Users(username=data.get("username"), email=data.get("email"))
        new_user.set_password(data.get("password"))
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        if 'users_email_key' in str(e.orig):
            return jsonify({"error": "Email already exists"}), 400
        elif 'users_username_key' in str(e.orig):
            return jsonify({"error": "Username already exists"}), 400
        else:
            return jsonify({"error": "An error occurred while creating the user"}), 500
        

@user_app_views.route('/users/<int:user_id>', methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """ Update user information """
    from api.views.db import Users
    from app import db
    from sqlalchemy.exc import IntegrityError
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        if "email" in data:
            existing_user = Users.query.filter_by(email=data["email"]).first()
            if existing_user and existing_user.userid != user_id:
                return jsonify({"error": "Email already exists"}), 400
            user.email = data["email"]
        
        if "username" in data:
            existing_user = Users.query.filter_by(username=data["username"]).first()
            if existing_user and existing_user.userid != user_id:
                return jsonify({"error": "Username already exists"}), 400
            user.username = data["username"]
        
        if "password" in data:
            user.set_password(data["password"])
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
    
    except IntegrityError as e:
        db.session.rollback()
        if 'users_email_key' in str(e.orig):
            return jsonify({"error": "Email already exists"}), 400
        elif 'users_username_key' in str(e.orig):
            return jsonify({"error": "Username already exists"}), 400
        else:
            return jsonify({"error": "An error occurred while updating the user"}), 500
        
@user_app_views.route('/users/<int:user_id>', methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """ Delete user by user ID """
    from api.views.db import Users
    from app import db

    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the user"}), 500