from aiogram import Router, types, filters

from backend.services.services import Services
from frontend.middlewares.admin_middleware import AdminCheckMiddleware


def poll_stats_route(services: Services, admin_mw: AdminCheckMiddleware) -> Router:
    router = Router()
    router.message.middleware(admin_mw.msg)
    router.callback_query.middleware(admin_mw.cb)

    POLL_ID_PREFIX = "stats_poll_"

    @router.message(filters.Command("stats"))
    async def stats(message: types.Message):
        polls = services.poll.get_all_polls()
        buttons = [
            [types.InlineKeyboardButton(text=e.poll.title, callback_data=POLL_ID_PREFIX+e.id)]
            for e in polls
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Выберите опрос:", reply_markup=keyboard)

    @router.callback_query(filters.Text(startswith=POLL_ID_PREFIX))
    async def poll_chosen(query: types.CallbackQuery):
        poll_id = query.data.removeprefix(POLL_ID_PREFIX)
        poll = services.poll.get_poll(poll_id) # TODO: handle None
        stats = services.stats.get_stats(poll_id)
        if not stats:
            await query.message.answer("Для этого опроса пока нет статистики.")
            return
        text = f"Статистика для опроса \"{poll.title}\"\n"
        for i, qstats in enumerate(stats.question_stats):
            text += f"{poll.questions[i].text}: Yes {qstats.yes}, No {qstats.no}, Idk {qstats.idk}\n"
        await query.message.answer(text)

        # TODO: factor out this part into a reusable function
        await query.answer()
        await query.message.delete_reply_markup()
        await query.message.edit_text(query.message.text + f'\nВыбран опрос {poll.title}')

    return router

