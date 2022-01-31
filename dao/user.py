from typing import Optional

import sqlalchemy.exc

from dao.model.genre import Genre
from dao.model.user import User
from exeptions import IncorrectData, DupLicateError


class UserDAO:
    def __init__(self, session):
        self.session = session
        self._roles = {'user', 'admin'}

    def get_one(self, bid):
        return self.session.query(User).get(bid)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).one_or_none()

    def get_all(self):
        return self.session.query(User).all()

    def create(self, genre_d):
        try:
            ent = User(**genre_d)
            self.session.add(ent)
            self.session.commit()
            return ent
        except sqlalchemy.exc.IntegrityError:
            raise DupLicateError

    def delete(self, rid):
        genre = self.get_one(rid)
        self.session.delete(genre)
        self.session.commit()

    def update_role(self, user_name: str, role: str):
        if role not in self._roles:
            raise IncorrectData

        user = self.get_by_username(user_name)
        user.role = role

        self.session.add(user)
        self.session.commit()

    def update_password(self, user_name: str, password_hash: str):

        user = self.get_by_username(user_name)
        user.password = password_hash

        self.session.add(user)
        self.session.commit()
        # genre = self.get_one(genre_d.get("id"))
        # genre.name = genre_d.get("name")
        #
        # self.session.add(genre)
        # self.session.commit()