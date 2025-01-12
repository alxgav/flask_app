import os

import pytest
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models import User, Expense


@pytest.fixture(scope="module")
def test_client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
    flask_app = create_app()

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client


@pytest.fixture(scope="module")
def new_user():
    return User(username="test", password="test")


@pytest.fixture(scope="module")
def init_database(test_client):
    db.create_all()
    default_user = User(
        username="test_user", password=generate_password_hash("test", method="pbkdf2")
    )

    second_user = User(
        username="second", password=generate_password_hash("test", method="pbkdf2")
    )

    db.session.add(default_user)
    db.session.add(second_user)
    db.session.commit()
    expense1 = Expense(title="test1", amount=100, user_id=default_user.id)
    expense2 = Expense(title="test2", amount=200, user_id=default_user.id)
    expense3 = Expense(title="test3", amount=300, user_id=default_user.id)
    db.session.add_all([expense1, expense2, expense3])
    db.session.commit()

    yield
    db.drop_all()


@pytest.fixture(scope="module")
def default_user_token(test_client):
    response = test_client.post(
        "/users/login", json={"username": "test_user", "password": "test"}
    )

    yield response.json["access_token"]


@pytest.fixture(scope="module")
def second_user_token(test_client):
    response = test_client.post(
        "/users/login", json={"username": "second", "password": "test"}
    )

    yield response.json["access_token"]
