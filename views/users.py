from flask import request
from flask_restx import Resource, Namespace
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest

from dao.model.user import UserSchema
from exeptions import DupLicateError
from implemented import user_service
from tools.auth import login_required
from tools.jwt_token import JwtSchema
from views.auth import LoginValidator

user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    @login_required
    def get(self, token_data):
        r = user_service.get_one(token_data['user_id'])
        return UserSchema().dump(r), 200

    def post(self):
        # Create user
        try:
            user_service.create(**LoginValidator().load(request.json))
        except ValidationError:
            raise BadRequest
        except DupLicateError:
            raise BadRequest('Username already exists')
