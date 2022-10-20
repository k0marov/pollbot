import asyncio
from typing import Callable, Coroutine, Any

import aiogram
from aiogram import types

from backend.services import poll_service
from backend.services.services import Services


# PollInviteSender is an async function that sends a message with a poll invitation to the given chat id
PollInviteSender = Callable[[str, poll_service.PollEntity], Coroutine[Any, Any, None]]

ACCEPT_POLL_CB_PREFIX = "accept_poll_"

def poll_invite_sender_factory(bot: aiogram.Bot) -> PollInviteSender:
    async def invite_sender(chat_id: str, poll: poll_service.PollEntity) -> None:
        print("inviting user %s" % chat_id)
        cb_data = ACCEPT_POLL_CB_PREFIX + poll.id
        buttons = [[aiogram.types.InlineKeyboardButton(text="OK", callback_data=cb_data)]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await bot.send_message(chat_id, "Пожалуйста, поучавствуйте в опросе.", reply_markup=keyboard) # TODO: add poll title

    return invite_sender
