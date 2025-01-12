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
        "NotFound": {
            "type": "object",
            "discriminator": "notFoundType",
            "properties": {"error": {"type": "string"}},
            "example": {"error": " We can't found it :("},
        },
    }
    return swg
