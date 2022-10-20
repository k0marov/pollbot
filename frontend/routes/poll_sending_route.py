from typing import Callable

import aiogram
from aiogram import Router, filters, types

from backend.services import poll_service
from backend.services.services import Services


ACCEPT_POLL_CB_PREFIX = "accept_poll_"

# TODO: maybe move poll saving from a db to the aiogram's state or some other built-in feature.
#  This will make it easier to implement every admin having its own poll list.

def poll_sending_route(services: Services, send_poll_invite: Callable[[str, poll_service.Poll], None]) -> Router:
    router = Router()

    @router.message(filters.Command("send_poll"))
    async def admin_send_poll_handler(message: types.Message):
        id = message.text.removeprefix("/send_poll").strip() # TODO: proper way of sending polls (without bothering the user with using the ids)
        poll = services.poll.get_poll(id)
        if not poll: return await message.answer("Опроса с таким id не найдено.")
        all_users = [user for user in services.user.get_all_users() if user != str(message.chat.id)]
        map(lambda user: send_poll_invite(user, poll), all_users)
        await message.answer("Приглашение поучавствовать в опросе было отправлено в %d чатов" % len(all_users))

    # async def _send_poll_invite_to_user(chat_id: str, poll: poll_service.Poll):
    #     cb_data = ACCEPT_POLL_CB_PREFIX + poll.id
    #     buttons = [[types.InlineKeyboardButton(text="OK", callback_data=cb_data)]]
    #     keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    #     await bot.send_message(chat_id, "Пожалуйста, поучавствуйте в опросе.", reply_markup=keyboard) # TODO: add poll title

    return router
