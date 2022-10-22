from aiogram import Router, types, filters

from backend.services.services import Services


def poll_stats_route(services: Services) -> Router:
    router = Router()

    @router.message(filters.Command("stats"))
    async def stats(message: types.Message):
        poll_id = message.text.removeprefix("/stats").strip()
        poll = services.poll.get_poll(poll_id) # TODO: handle None
        stats = services.poll.get_stats(poll_id)
        text = f"Статистика для опроса \"{poll.poll.title}\"\n"
        for question, qstats in stats.question_stats:
            text += f"{question.text}: Yes {qstats.yes}, No {qstats.no}, Idk {qstats.idk}\n"
        await message.answer(text)

    return router

