import datetime
from abc import ABC, abstractmethod
from typing import Optional, List

from hseduck_bot.model.portfolios import Portfolio
from hseduck_bot.model.users import User

STATUS_BEFORE = 0
STATUS_RUNNING = 1
STATUS_FINISHED = 2


class Contest:
    def __init__(self, name: str, owner_id: int, start_date: datetime.datetime, end_date: datetime.datetime,
                 status: int = STATUS_BEFORE,
                 contest_id: Optional[int] = None):
        self.name = name
        self.owner_id = owner_id
        self.status = status
        self.start_date = start_date
        self.end_date = end_date
        self.id = contest_id


class Participation:
    def __init__(self, user_id: int, contest_id: int):
        self.user_id = user_id
        self.contest_id = contest_id


class ContestStorage(ABC):
    @abstractmethod
    def new_contest(self, contest: Contest) -> None:
        pass

    @abstractmethod
    def get_participants_by_contest_id(self, contest_id: int) -> List[User]:
        pass

    @abstractmethod
    def get_contests_for_user_id(self, user_id: int) -> List[Contest]:
        pass

    @abstractmethod
    def get_owned_contests_for_user_id(self, user_id: int) -> List[Contest]:
        pass

    @abstractmethod
    def join_contest(self, user_id: int, contest_id: int) -> None:
        pass

    @abstractmethod
    def is_participant(self, user_id: int, contest_id: int) -> bool:
        pass

    @abstractmethod
    def update_all_contests(self, timestamp: datetime.datetime) -> None:
        pass

    @abstractmethod
    def get_contest_by_id(self, contest_id) -> Optional[Contest]:
        pass

    @abstractmethod
    def get_contest_portfolio_for_user_id(self, user_id: int, contest_id: int) -> Optional[Portfolio]:
        pass
