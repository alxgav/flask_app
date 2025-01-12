from flask_swagger import swagger


def build_swagger(app):
    swg = swagger(app)
    swg["info"]["title"] = "app for controls expenses"
    swg["info"]["version"] = "0.0.1"
    swg["definitions"] = {
        "Hello": {
            "type": "object",
            "discriminator": "helloType",
            "properties": {"message": {"type": "string"}},
            "example": {"message": "Hi, I'm your app for controls expenses!"},
        },
        "ExpenseIn": {
            "type": "object",
            "discriminator": "expenseInType",
            "properties": {
                "title": {"type": "string"},
                "amount": {"type": "number"},
            },
            "example": {
                "title": "I'm your expense",
                "amount": 0,
            },
        },
        "ExpenseOut": {
            "allOf": [
                {"$ref": "#/definitions/ExpenseIn"},
                {
                    "type": "object",
                    "properties": {
                        "id": {"type": "number"},
                    },
                    "example": {
                        "id": 0,
                    },
                },
            ],
        },
        "UserIn": {
            "type": "object",
            "discriminator": "userInType",
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "example": {
                "username": "I'm your user",
                "password": "I'm your password",
            },
        },
        "UserOut": {
            "type": "object",
            "discriminator": "userOutType",
            "properties": {
                "id": {"type": "number"},
                "username": {"type": "string"},
            },
            "example": {
                "id": 0,
                "username": "I'm your user",
            },
        },
        "Unauthorized": {
            "type": "object",
            "discriminator": "unauthorizedType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": "You don't have permission for this expense"},
        },
        "TokenOut": {
            "type": "object",
            "discriminator": "tokenOutType",
            "properties": {"token": {"type": "string"}},
        },
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": " We can't found it :("},
        },
    }
    return swg
