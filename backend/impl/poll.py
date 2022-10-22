import dataclasses
import typing
from typing import List

from backend.services import poll
from backend.services.poll import PollEntity, Poll
from backend.store import store

class PollServiceImpl(poll.PollService):
    def __init__(self, s: store.Store):
        self._store = s

    _POLLS_KEY = "polls"

    def create_poll(self, poll: Poll) -> str:
        polls = self.get_all_polls()
        new_id = str(len(polls))
        polls.append(PollEntity(new_id, poll))
        self._store.set(self._POLLS_KEY, self._polls_to_json(polls))
        return new_id

    def get_poll(self, poll_id: str) -> typing.Optional[Poll]:
        polls = self.get_all_polls()
        if 0 <= int(poll_id) < len(polls): # TODO: handle non-int ids
            return polls[int(poll_id)].poll
        return None

    def get_all_polls(self) -> List[PollEntity]:
        result = self._store.get(PollServiceImpl._POLLS_KEY)
        return self._polls_from_json(result) if result else []

    def _poll_from_json(self, json: typing.Dict[str, typing.Any]) -> Poll:
        return Poll(
            title=json.get("title"),
            questions=[poll.Question(text=q) for q in json.get("questions")],
        )
    def _polls_from_json(self, json: typing.Any) -> List[PollEntity]:
        return [PollEntity(str(ind), self._poll_from_json(p)) for ind, p in enumerate(json)]
    def _poll_to_json(self, poll: Poll) -> typing.Dict[str, typing.Any]:
        return {
            "title": poll.title,
            "questions": [q.text for q in poll.questions],
        }
    def _polls_to_json(self, polls: List[PollEntity]) -> typing.List[typing.Dict[str, typing.Any]]:
        return [self._poll_to_json(poll.poll) for poll in polls]

    # def _stats_from_json(self, json: typing.Dict[str, typing.Any]) -> typing.Dict[str, PollStatsModel]:
    #     return {
    #       k: v for k, v in json
    #     }
    # def _stats_model_from_json(self, json: typing.Dict[str, typing.Any]) -> PollStatsModel:
    #     return PollStatsModel({
    #         id: poll.AnswerStats(yes=ans[Answer.YES], no=ans[Answer.NO], idk=ans[Answer.IDK]) for id, ans in json.get("questions")
    #     })



