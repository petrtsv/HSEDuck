import datetime
from typing import Optional, List, Tuple

from hseduck_bot import config
from hseduck_bot.controller import transactions, portfolios, users
from hseduck_bot.model import contests as contests_model
from hseduck_bot.model.contests import ContestStorage, Contest
from hseduck_bot.model.portfolios import Portfolio
from hseduck_bot.model.users import User

contest_storage: Optional[ContestStorage] = None


def initialize(storage: ContestStorage):
    global contest_storage
    contest_storage = storage


def create_contest(user_id: int, name: str, start_date: datetime.datetime, end_date: datetime.datetime,
                   must_join: bool = True) -> Contest:
    new_contest = Contest(name=name, owner_id=user_id, start_date=start_date, end_date=end_date,
                          status=contests_model.STATUS_BEFORE)
    contest_storage.new_contest(new_contest)
    if must_join:
        join_contest(user_id, new_contest.id)
    return new_contest


def get_by_id(contest_id: int) -> Optional[Contest]:
    return contest_storage.get_contest_by_id(contest_id)


def list_contests_for_user_id(user_id: int) -> List[Contest]:
    return contest_storage.get_contests_for_user_id(user_id)


def list_owned_contests_for_user_id(user_id: int) -> List[Contest]:
    return contest_storage.get_owned_contests_for_user_id(user_id)


def join_contest(user_id: int, contest_id: int) -> None:
    contest = get_by_id(contest_id)
    if contest is None:
        return
    if contest.status == contests_model.STATUS_FINISHED:
        raise InvalidContestStateError(contest)
    contest_storage.join_contest(user_id, contest.id)
    portfolios.create_portfolio(user_id, contest.name, contest_id=contest.id)


def get_global_contest_id() -> int:
    if not users.check_existence(config.GLOBAL_CONTEST_OWNER_USERNAME):
        raise ValueError('Cannot find GLOBAL contest')
    global_contest_owner = users.login(config.GLOBAL_CONTEST_OWNER_USERNAME)
    global_contest_owner_contests = list_owned_contests_for_user_id(global_contest_owner.id)
    if len(global_contest_owner_contests) < 1:
        raise ValueError('Cannot find GLOBAL contest')
    global_contest = global_contest_owner_contests[0]
    return global_contest.id


def join_global(user_id: int) -> None:
    join_contest(user_id, global_contest.id)


def get_contest_results(contest_id: int) -> List[Tuple[float, User, Portfolio]]:
    participants = contest_storage.get_participants_by_contest_id(contest_id)
    participants_portfolios = [contest_storage.get_contest_portfolio_for_user_id(user_id=user.id, contest_id=contest_id)
                               for user in participants]
    participants_results = [transactions.portfolio_total_cost(portfolio.id) for portfolio in
                            participants_portfolios]
    results = list(zip(participants_results, participants, participants_portfolios))
    results.sort(key=lambda e: (e[0], e[1].username), reverse=True)
    return results


def get_contest_result_by_user_id(contest_id: int, user_id: int) -> Optional[Tuple[int, float]]:
    results = get_contest_results(contest_id)
    for i, row in enumerate(results):
        if row[1].id == user_id:
            return i, row[0]
    return None


def is_participant(user_id: int, contest_id: int) -> bool:
    return contest_storage.is_participant(contest_id=contest_id, user_id=user_id)


def update() -> None:
    contest_storage.update_all_contests(datetime.datetime.now())


def create_global_competition() -> None:
    need_to_create = not users.check_existence(config.GLOBAL_CONTEST_OWNER_USERNAME)
    if need_to_create:
        user = users.login(config.GLOBAL_CONTEST_OWNER_USERNAME)
        start_date = datetime.datetime.now()
        end_date = datetime.datetime.now() + config.GLOBAL_COMPETITION_DURATION
        global_contest = create_contest(user.id, start_date=start_date, end_date=end_date,
                                        name=config.GLOBAL_COMPETITION_NAME,
                                        must_join=False)
        print("Created global contest: name = %s, id = %d, end_date = %s" % (
            global_contest.name, global_contest.id, str(global_contest.end_date)))


class InvalidContestStateError(Exception):
    def __init__(self, contest):
        super(InvalidContestStateError, self).__init__()
        self.contest = contest
