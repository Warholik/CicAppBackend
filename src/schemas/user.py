from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "user_name": {
            "type": "string",
            "maxLength": 20
        },
        "email": {
            "type": "string",
            "format": "email",
            "maxLength": 20
        },
        "password": {
            "type": "string",
            "minLength": 5,
            "maxLength": 20
        }
    },
    "required": ["email", "password"],
    "additionalProperties": False
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}