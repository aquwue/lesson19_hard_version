from functools import wraps
from typing import Any, Dict

from flask import request, current_app
from flask_restx import abort
from jwt import PyJWTError
import jwt
from tools.jwt_token import JwtToken, JwtSchema
from marshmallow import ValidationError


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        aut_header = request.headers.get("Authorization")
        if not aut_header:
            abort(401)

        try:
            data = JwtToken.decode_token(aut_header.split("Bearer ")[-1])
            # data.pop("exp", None)
            token_data: Dict[str, Any] = JwtSchema().load(data)
            return func(*args, **kwargs, token_data=token_data)
        except (PyJWTError, ValidationError) as e:
            print("1")
            print(str(e))
            abort(401)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        aut_header = request.headers.get("Authorization")
        if not aut_header:
            abort(401)

        try:
            data = JwtToken.decode_token(aut_header.split("Bearer")[-1])
            # data.pop("exp", None)
            token_data: Dict[str, Any] = JwtSchema().load(data)
            if token_data['role'] != 'admin':
                abort(403)
            return func(*args, **kwargs, token_data=token_data)
        except (PyJWTError, ValidationError):
            abort(401)

    return wrapper


def auth_required(func):
    def wrapper(*args, **kwargs):
        if 'Authorization' not in request.headers:
            abort(401)

        data = request.headers['Authorization']
        token = data.split("Bearer ")[-1]
        try:
            jwt.decode(token, current_app.config['SECRET_HERE'], algorithms=['HS256'])
        except Exception as e:
            print("JWT Decode Exception", e)
            abort(401)
        return func(*args, **kwargs)

    return wrapper
