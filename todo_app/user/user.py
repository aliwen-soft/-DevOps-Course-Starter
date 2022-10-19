from flask_login import UserMixin
from enum import Enum
from functools import wraps
from flask_login import current_user


class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.role = user_mapping[id] if id in user_mapping.keys() else UserRoles.READER


class UserRoles(Enum):
    READER = 0
    WRITER = 1


user_mapping = {
    "74604620": UserRoles.WRITER
}


def requireWriter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if isWriter:
            return func(*args, **kwargs)
        else:
            return {"message": "you are not authorized to use that"}, 401
    return wrapper


def isWriter():
    return current_user.is_anonymous or current_user.role == UserRoles.WRITER
