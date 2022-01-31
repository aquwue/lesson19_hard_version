from datetime import datetime, timedelta
from typing import Dict, Any
from calendar import timegm
import jwt
from flask import current_app
from marshmallow import Schema, fields


class JwtSchema(Schema):
    user_id = fields.Int(required=True)
    role = fields.Str(required=True)
    exp = fields.Int()


class JwtToken:
    def __init__(self, data: Dict[str, Any]):
        self.now = datetime.now()
        self.data = data
        self.access_token_expiration = 10
        self.refresh_token_expiration = 30

    def _get_token(self, time_delta: timedelta) -> str:
        self.data.update({
            "exp": timegm((self.now + time_delta).timetuple())
        })
        return jwt.encode(self.data, current_app.config['SECRET_HERE'], algorithm='HS256')

    def _refresh_token(self) -> str:
        return self._get_token(time_delta=timedelta(days=self.refresh_token_expiration))

    def _access_token(self) -> str:
        return self._get_token(time_delta=timedelta(minutes=self.access_token_expiration))

    def get_tokens(self) -> Dict[str, str]:
        return {
            "access_token": self._access_token(),
            "refresh_token": self._refresh_token()
        }

    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        return jwt.decode(token, current_app.config['SECRET_HERE'], algorithms=['HS256'])
