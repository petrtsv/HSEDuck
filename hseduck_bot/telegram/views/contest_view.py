from typing import Optional

from hseduck_bot.controller import contests
from hseduck_bot.model import contests as contests_model
from hseduck_bot.model.contests import Contest
from hseduck_bot.telegram.commands.utils import money_to_str
from hseduck_bot.telegram.template_utils import get_text, make_bold


def status_view(status: int):
    if status == contests_model.STATUS_BEFORE:
        return "BEFORE"
    elif status == contests_model.STATUS_RUNNING:
        return "RUNNING"
    elif status == contests_model.STATUS_FINISHED:
        return "FINISHED"
    return "UNKNOWN"


def contest_view(contest: Contest, user_id: Optional[int] = None):
    results = []
    for i, row in enumerate(contests.get_contest_results(contest.id)):
        row_text = get_text("contest_result", {
            'place': i + 1,
            'username': row[1].username,
            'price': money_to_str(row[0])
        })
        if row[1].id == user_id:
            row_text = make_bold(row_text)
        results.append(row_text)
    results_text = "\n\n".join(results)
    return get_text("contest_info", {
        'results': results_text,
        'name': contest.name,
        'status': status_view(contest.status),
        'deadline': contest.end_date.strftime("%Y-%m-%d %H:%M:%S %Z%z")
    })
