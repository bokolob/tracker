from functools import wraps

import jsonschema
from flask import request, jsonify, make_response
from werkzeug.exceptions import abort

validators = {
    '/devices/add': jsonschema.Draft7Validator({
        'type': 'object',
        'required': ['imei','name'],
        'additionalProperties': False,
        'properties': {
            'imei': {
                'pattern': "^[^\\s]+$",
                'type': 'string',
                'minLength': 5,
                'maxLength': 32,
                "error_msg": "Imei is incorrect"
            },
            'name': {
                'pattern': "^[^\\s]+$",
                'type': 'string',
                'maxLength': 32,
                "error_msg": "Name is incorrect"
            },
        }
    }),
    '/auth': jsonschema.Draft7Validator({
        'type': 'object',
        'required': ['email', 'password'],
        'additionalProperties': False,
        'properties': {
            'email': {
                'type': 'string',
                'pattern': '\\S+\\@\\S+\\.\\S+',
                'maxLength': 32,
                "error_msg": "Email is incorrect"
            },
            'password': {
                'pattern': "[^\\s]+",
                'type': 'string',
                "error_msg": "Password must be string without spaces"
            }
        }
    }),
    '/signup': jsonschema.Draft7Validator({
        'type': 'object',
        'required': ['email', 'password', 'imei', 'password_confirm'],
        'additionalProperties': False,
        'properties': {
            'email': {
                'type': 'string',
                'pattern': '\\S+\\@.+\\.\\S+',
                'minLength': 5,
                'maxLength': 32,
                "error_msg": "Email is incorrect"
            },
            'password': {
                'pattern': "^[^\\s]+$",
                'type': 'string',
             #   'minLength': 8,
             #   'maxLength': 16,
                "error_msg": "Password is too short or too long"
            },
            'password_confirm': {
                'pattern': "^[^\\s]+$",
                'type': 'string',
                'minLength': 8,
                'maxLength': 16,
                "error_msg": "Repeated password is too short or too long"
            },
            'imei': {
                'pattern': "^[^\\s]+$",
                'type': 'string',
                'minLength': 5,
                'maxLength': 32,
                "error_msg": "Imei is incorrect"
            },
        }
    }),

}


def validated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = {}

        errors = validators[request.url_rule.rule].iter_errors(request.get_json())

        for err in errors:
            response[".".join(err.absolute_path)] = err.schema.get('error_msg', err.message)

        if len(response) != 0:
            abort(make_response(jsonify({'errors': response}), 400))

        return f(*args, **kwargs)

    return decorated_function
