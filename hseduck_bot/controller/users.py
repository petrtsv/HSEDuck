from typing import Optional

from hseduck_bot.model.users import UserStorage, User

user_storage: Optional[UserStorage] = None


def initialize(storage: UserStorage):
    global user_storage
    user_storage = storage


def login(username: str) -> User:
    user = User(username)
    user_storage.find_user(user, create=True)
    return user

