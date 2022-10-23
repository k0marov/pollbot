import typing

from lib.backend.services import stats
from lib.backend.services.stats import PollStats, Answer, AnswerStats
from lib.backend.store import store


class StatsServiceImpl(stats.StatsService):
    def __init__(self, s: store.Store):
        self._store = s

    _STATS_PREFIX = "stats_"

    def record_answer(self, poll_id: str, question_id: int, answer: Answer, poll_len: int) -> None:
        stats = self.get_stats(poll_id)
        if not stats: stats = PollStats([AnswerStats(0,0,0) for answer in range(poll_len)])
        if answer == Answer.YES:
            stats.question_stats[question_id].yes += 1
        elif answer == Answer.NO:
            stats.question_stats[question_id].no += 1
        elif answer == Answer.IDK:
            stats.question_stats[question_id].idk += 1
        self._store.set(self._STATS_PREFIX+poll_id, self._stats_to_json(stats))

    def get_stats(self, poll_id: str) -> typing.Optional[PollStats]:
        stats = self._store.get(self._STATS_PREFIX+poll_id)
        return self._stats_from_json(stats) if stats else None

    def _stats_from_json(self, json: typing.List[typing.Dict[str, typing.Any]]) -> PollStats:
        return PollStats([self._answer_stats_from_json(answer) for answer in json])
    def _answer_stats_from_json(self, json: typing.Dict[str, typing.Any]) -> AnswerStats:
        return AnswerStats(
            yes=json.get('yes'),
            no=json.get('no'),
            idk=json.get('idk')
        )

    def _stats_to_json(self, stats: PollStats) -> typing.List[typing.Dict[str, typing.Any]]:
        return [{"yes": q.yes, "no": q.no, "idk": q.idk} for q in stats.question_stats]
