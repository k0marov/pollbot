import asyncio

from aiogram import Router, filters, types

from lib.backend.services.poll import PollEntity
from lib.backend.services.services import Services
from lib.frontend.design.texts import Texts
from lib.frontend.middlewares.admin_middleware import AdminCheckMiddleware
from lib.frontend.routes import poll_answering_route


# TODO: maybe move poll saving from a db to the aiogram's state or some other built-in feature.
#  This will make it easier to implement every admin having its own poll list.

def poll_sending_route(services: Services, send_poll_invite: poll_answering_route.PollInviteSender, admin_mw: AdminCheckMiddleware) -> Router:
    router = Router()
    router.message.middleware(admin_mw.msg)
    router.callback_query.middleware(admin_mw.cb)

    POLL_ID_PREFIX = "select_poll_"

    @router.message(filters.Command("send_poll"))
    async def admin_send_poll_handler(message: types.Message):
        # TODO: remove code duplication with poll_stats_route
        polls = services.poll.get_all_polls()
        buttons = [
            [types.InlineKeyboardButton(text=e.poll.title, callback_data=POLL_ID_PREFIX+e.id)]
            for e in polls
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(Texts.CHOOSE_POLL, reply_markup=keyboard)

    @router.callback_query(filters.Text(startswith=POLL_ID_PREFIX))
    async def poll_selected_handler(query: types.CallbackQuery):
        id = query.data.removeprefix(POLL_ID_PREFIX)
        poll = services.poll.get_poll(id)
        if not poll: return await query.message.answer(Texts.NO_POLL)
        all_users = [user for user in services.user.get_all_users() if user != str(query.message.chat.id)]

        # TODO: maybe there should be a timeout here to escape the 429 Too Many Requests error
        await asyncio.gather(*[send_poll_invite(user, PollEntity(id=id, poll=poll)) for user in all_users])

        await query.message.answer(Texts.INVITATIONS_REPORT(len(all_users)))
        await query.answer()
        await query.message.delete_reply_markup()
        await query.message.edit_text(query.message.text + Texts.CHOSEN_POLL(poll))

    return router
