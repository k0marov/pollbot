import asyncio
from typing import Callable, Coroutine, Any

import aiogram
from aiogram import types, Router, filters
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext

from backend.services import poll_service
from backend.services.services import Services


class PollAnswering(state.StatesGroup):
    answering_question = state.State()


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

def poll_answering_route(services: Services) -> Router:
    router = Router()

    POLL_ID_KEY = "POLL_ID"
    QUESTION_ID_KEY = "QUESTION_ID"

    @router.callback_query(filters.Text(startswith=ACCEPT_POLL_CB_PREFIX))
    async def accept_poll_callback(query: types.CallbackQuery, state: FSMContext):
        poll_id = query.data.removeprefix(ACCEPT_POLL_CB_PREFIX)
        poll = services.poll.get_poll(poll_id) # TODO: handle None
        question_id = 0
        await state.set_state(PollAnswering.answering_question)
        await state.set_data({POLL_ID_KEY: poll_id, QUESTION_ID_KEY: question_id})
        await query.answer()

        await query.message.answer(poll.poll.questions[question_id].text)


    return router

