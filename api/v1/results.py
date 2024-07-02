from flask import Blueprint, jsonify, abort, request
# from api.v1 import app_views

result_app_views = Blueprint('result_app_views', __name__, url_prefix='/api/v1')


@result_app_views.route("/results", methods=["GET"], strict_slashes=False)
def get_user_results():
    """ Retrieves the list of all user results objects
    """
    from api.views.db import QuizResults
    results = QuizResults.query.all()

    return jsonify([result.to_dict() for result in results])


@result_app_views.route("/results/details/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_result_details_by_userid(user_id):
    """ Retrieves the details of a user result object
    """
    from api.views.db import QuizResults
    result_details = QuizResults.query.filter_by(userid=user_id).all()

    return jsonify([result_detail.to_dict_details() for result_detail in result_details])