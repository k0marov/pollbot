from aiogram import Router, types, filters

from backend.services.services import Services
from frontend.middlewares.admin_middleware import AdminCheckMiddleware


def poll_stats_route(services: Services, admin_mw: AdminCheckMiddleware) -> Router:
    router = Router()
    router.message.middleware(admin_mw.msg)
    router.callback_query.middleware(admin_mw.cb)

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

