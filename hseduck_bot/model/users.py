from abc import ABC, abstractmethod
from typing import Optional


class User:
    def __init__(self, username: str, user_id: int = None):
        self.id = int(user_id) if user_id is not None else None
        self.username = username


class UserStorage(ABC):
    @abstractmethod
    def create_user(self, user: User) -> None:
        pass

    @abstractmethod
    def find_user(self, user: User, create: bool = False) -> None:
        """
        Find user with specified username in database, set id of the passed User object.
        :param user: User object to use username of. Set user.id after finding row with specified username.
        :param create: (default: False) Create user
        :return: None
        """
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass
