from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import ValidationError

from app.db import db
from app.models import Expense
from app.schemas import expense_schema, expenses_schema

bp = Blueprint("expense", __name__, url_prefix="/expenses")


@bp.route("/", methods=["GET"])
@jwt_required()
def get_expenses():
    """
    Get list of expenses
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: Authorization
      in: header
      description: Bearer token
      required: true
    responses:
          200:
            description: List of expenses
            schema:
                type: array
                items:
                    $ref: '#/definitions/ExpenseOut'
    """
    return jsonify(expenses_schema.dump(current_user.expenses)), 200


@bp.route("/<int:id>", methods=["GET"])
@jwt_required()
def get_expense(id):
    """
    get data of expense by id
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: Authorization
      in: header
      description: Bearer token
      required: true
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
    if expense.user_id != current_user.id:
        return jsonify(error="You don't have permission for this expense"), 401
    return jsonify(expense_schema.dump(expense)), 200


@bp.route("/", methods=["POST"])
@jwt_required()
def create_expenses():
    """
    Create new expense
    ---
    tags:
        - expenses
    produces:
        - application/json

    parameters:
    - name: Authorization
      in: header
      description: Bearer token
      required: true
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

    new_expense = Expense(
        title=data["title"], amount=data["amount"], user_id=current_user.id
    )
    db.session.add(new_expense)
    db.session.commit()
    return jsonify(expense_schema.dump(new_expense)), 201


@bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def update_expenses(id):
    """
    update data of expense by id
    ---
    tags:
        - expenses
    produces:
        - application/json
    parameters:
    - name: Authorization
      in: header
      description: Bearer token
      required: true
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
    if expense.user_id != current_user.id:
        return jsonify(error="You don't have permission for this expense"), 401
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
        - expenses
    produces:
        - application/json
    parameters:
    - name: Authorization
      in: header
      description: Bearer token
      required: true
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
    if expense.user_id != current_user.id:
        return jsonify(error="You don't have permission for this expense"), 401
    if expense is None:
        return {"message": "Expense not found"}, 404

    db.session.delete(expense)
    db.session.commit()
    return "", 204
