from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "lastName": {
            "type": "string",
        },
        "email": {
            "type": "string",
            "format": "email",
        },
        "password": {
            "type": "string",
            "minLength": 5
        },
        "photoUrl": {
            "type": "string",
        },
        "role":{
            "type" : "string",
            "enum" : ["admin", "operator","customer"]
        }

    },
    "required": ["email", "name", "lastName", "role"],
    "additionalProperties": {
        "_id": {
            "type": "string",
        }
    }
}


def validate_user(data):
    try:
        validate(data, user_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}

    