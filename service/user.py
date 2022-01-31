from typing import Optional

from dao.model.user import User
from dao.user import UserDAO
from tools.security import get_password_hash


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, bid):
        return self.dao.get_one(bid)

    def get_by_name(self, username: str) -> Optional[User]:
        return self.dao.get_by_username(username)

    def create(self, username, password, role: str = "user"):
        self.dao.create({
            "username": username,
            "password": get_password_hash(password),
            "role": role,
        })
