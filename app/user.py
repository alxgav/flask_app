from flask import request, jsonify, Blueprint
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db
from app.models import User
from app.schemas import user_schema
from flask_jwt_extended import create_access_token

bp = Blueprint("user", __name__, url_prefix="/users")


@bp.route("/", methods=["POST"])
def register_user():
    json_data = request.json
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    try:
        new_user = User(
            username=data["username"], password=generate_password_hash(data["password"])
        )
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as err:
        db.session.rollback()
        return jsonify(error="User already exists"), 400

    return jsonify(user_schema.dump(new_user)), 201


@bp.route("/login", methods=["POST"])
def login_user():
    json_data = request.json
    try:
        data = user_schema.load(json_data)
    except ValidationError as err:
        return jsonify(err.messages), 422

    user = db.first_or_404(db.select(User).filter_by(username=data["username"]))
    if not check_password_hash(user.password, data["password"]):
        return jsonify(error="Invalid password or username"), 401
    access_token = create_access_token(identity=user.username)
    return jsonify(access_token=access_token), 200


# @bp.route("/logout", methods=["POST"])
# def logout_user():
#     token = request.headers.get("Authorization").split(" ")[1]  # Assuming Bearer token
#     blacklist.add(token)  # Add token to blacklist
#     return "", 204
