from pyexpat.errors import messages


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from db_helper import db

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY="dev")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///expenses.db"
db.init_app(app)


@app.route("/")
def home():
    return jsonify(message="Hello from API v1")


@app.route("/expenses/", methods=["POST"])
def create_expenses():
    pass


@app.route("/expenses/", methods=["GET"])
def get_expenses():
    pass


@app.route("/expenses/<int:id>", methods=["GET"])
def get_expense(id):
    pass


@app.route("/expenses/<int:id>", methods=["PATCH"])
def update_expenses(id):
    pass


@app.route("/expenses/<int:id>", methods=["DELETE"])
def delete_expenses(id):
    pass


if __name__ == "__main__":
    app.run()
