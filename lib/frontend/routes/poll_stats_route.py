from aiogram import Router, types, filters

from lib.backend.services.services import Services
from lib.frontend.design.texts import Texts
from lib.frontend.middlewares.admin_middleware import AdminCheckMiddleware


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
        await message.answer(Texts.CHOOSE_POLL, reply_markup=keyboard)

    @router.callback_query(filters.Text(startswith=POLL_ID_PREFIX))
    async def poll_chosen(query: types.CallbackQuery):
        poll_id = query.data.removeprefix(POLL_ID_PREFIX)
        poll = services.poll.get_poll(poll_id)
        if not poll: return await query.message.answer(Texts.NO_POLL)
        stats = services.stats.get_stats(poll_id)
        if not stats: return await query.message.answer(Texts.NO_STATS)
        await query.message.answer(Texts.STATS(poll, stats))

        # TODO: factor out this part into a reusable function
        await query.answer()
        await query.message.delete_reply_markup()
        await query.message.edit_text(query.message.text + Texts.CHOSEN_POLL(poll))

    return router

