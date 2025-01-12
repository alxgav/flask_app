from flask import Blueprint, request, jsonify
from marshmallow import ValidationError

from app.db import db
from app.models import Expense
from app.schemas import expense_schema, expenses_schema

bp = Blueprint("expense", __name__, url_prefix="/expenses")


@bp.route("/", methods=["GET"])
def get_expenses():
    """
    Get list of expenses
    ---
    tags:
        - expenses
    produces:
        - application/json
    responses:
          200:
            description: List of expenses
            schema:
                type: array
                items:
                    $ref: '#/definitions/ExpenseOut'
    """
    expenses = Expense.query.all()
    return jsonify(expenses_schema.dump(expenses)), 200


@bp.route("/<int:id>", methods=["GET"])
def get_expense(id):
    """
    get data of expense by id
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: expense id
      required: true
      type: number
    responses:
        200:
            description: Found expense
            schema:
                $ref: '#/definitions/ExpenseOut'
        404:
            description: not found expense by id
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/", methods=["POST"])
def create_expenses():
    """
    Create new expense
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: expense
      in: body
      description: Data of expense
      required: true
      schema:
        $ref: '#/definitions/ExpenseIn'
    responses:
        201:
            description: Expense created
            schema:
                $ref: '#/definitions/ExpenseOut'
    """
    json_data = request.json
    try:
        data = expense_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422

    new_expense = Expense(title=data["title"], amount=data["amount"])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(expense_schema.dump(new_expense)), 201


@bp.route("/<int:id>", methods=["PATCH"])
def update_expenses(id):
    """
    update data of expense by id
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: idy of expense
      required: true
      type: number
    - name: expense
      in: body
      description: data for update expense
      required: true
      schema:
        $ref: '#/definitions/ExpenseIn'
    responses:
        200:
            description: Updated expense
            schema:
                $ref: '#/definitions/ExpenseOut'
        404:
            description: not found expense by id
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.get_or_404(Expense, id)
    json_data = request.json
    try:
        data = expense_schema.load(json_data, partial=True)
    except ValidationError as err:
        return err.messages, 422
    expense.title = data.get("title", expense.title)
    expense.amount = data.get("amount", expense.amount)
    db.session.commit()
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/<int:id>", methods=["DELETE"])
def delete_expenses(id):
    """
    Delete expense
    ---
    tags:
        - expense
    produces:
        - application/json
    parameters:
    - name: id
      in: path
      description: ID of the expense
      required: true
      type: integer
    responses:
        204:
            description: Expense deleted
        404:
            description: Expense not found by ID
            schema:
                $ref: '#/definitions/NotFound'
    """
    expense = db.session.get(Expense, id)
    if expense is None:
        return {"message": "Expense not found"}, 404

    db.session.delete(expense)
    db.session.commit()
    return "", 204
