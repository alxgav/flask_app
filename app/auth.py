from flask_jwt_extended import JWTManager

from app.models import User

jwt = JWTManager()


@jwt.user_identity_loader
def user_identity(username):
    return username


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = user_identity(jwt_data["sub"])
    return User.query.filter_by(username=identity).one_or_none()
