import os

from flask import Flask, jsonify

from app import expense, user
from app.db import db
from app.migrate import migrate
from app.schemas import user_schema
from app.swagger_bp import SWAGGER_API_URL, swagger_ui_blueprint
from app.swagger_utils import build_swagger

from app.auth import jwt


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_type = os.getenv("CONFIG_TYPE", default="app.config.Config")
    app.config.from_object(config_type)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

    @app.route(SWAGGER_API_URL)
    def spec():
        return jsonify(build_swagger(app))

    @app.route("/")
    def home():
        """
        Welcome user to main page
        ---
        tags:
            - main page
        produces:
            - application/json
        responses:
            200:
                description: Welcome
                schema:
                    $ref: '#/definitions/Hello'
        """
        return jsonify(message="Hello from API v1")

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({"error": "Server Error"}), 500

    # register blueprints
    app.register_blueprint(expense.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(swagger_ui_blueprint)

    # jwt

    jwt.init_app(app)

    return app
