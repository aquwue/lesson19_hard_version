import jwt
from flask import request, current_app
from flask_restx import Resource, Namespace, abort
from marshmallow import Schema, fields, ValidationError
from werkzeug.exceptions import BadRequest

from dao.model.genre import GenreSchema
from exeptions import DupLicateError
from implemented import user_service
from tools.auth import login_required, auth_required
from tools.jwt_token import JwtToken, JwtSchema

auth_ns = Namespace('auth')


class LoginValidator(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)


@auth_ns.route('/')
class AuthView(Resource):
    def post(self):
    # Create tokens
        try:
            validated_data = LoginValidator().load(request.json)
            print(validated_data)
            user = user_service.get_by_name(validated_data['username'])
            if not user:
                abort(404)

            token_data = JwtSchema().load({'user_id': user.id, 'role': user.role})

            return JwtToken(token_data).get_tokens(), 201

        except ValidationError:
            abort(400)

    @login_required
    def put(self, token_data):
        try:
            data = JwtSchema().load({'user_id': token_data['user_id'], 'role': token_data['role']})

            return JwtToken(data).get_tokens(), 201

        except ValidationError:
            abort(400)






#     @login_required
#     def get(self, token_data):
#         rs = genre_service.get_all()
#         res = GenreSchema(many=True).dump(rs)
#         return res, 200
#
#
# @auth_ns.route('/<int:rid>')
# class GenreView(Resource):
#     def get(self, rid):
#         r = genre_service.get_one(rid)
#         sm_d = GenreSchema().dump(r)
#         return sm_d, 200
