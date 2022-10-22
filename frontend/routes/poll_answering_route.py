import asyncio
from typing import Callable, Coroutine, Any

import aiogram
from aiogram import types, Router, filters
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext

from backend.services import poll_service
from backend.services.poll_service import Answer
from backend.services.services import Services

# TODO: move all of the text literals to a separate module as constants
# TODO: maybe get rid of PollEntity to reduce complexity


class PollAnswering(state.StatesGroup):
    answering_question = state.State()


# TODO: maybe just move this to the poll_sending_route to get rid of the typedef complexity
PollInviteSender = Callable[[str, poll_service.PollEntity], Coroutine[Any, Any, None]]
"""async function that sends a message with a poll invitation to the given chat id"""

ACCEPT_POLL_CB_PREFIX = "accept_poll_"

def poll_invite_sender_factory(bot: aiogram.Bot) -> PollInviteSender:
    async def invite_sender(chat_id: str, poll: poll_service.PollEntity) -> None:
        print("inviting user %s" % chat_id)
        cb_data = ACCEPT_POLL_CB_PREFIX + poll.id
        buttons = [[aiogram.types.InlineKeyboardButton(text="OK", callback_data=cb_data)]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        text = "Пожалуйста, поучавствуйте в опросе: " + poll.poll.title
        await bot.send_message(chat_id, text, reply_markup=keyboard)

    return invite_sender

def poll_answering_route(services: Services) -> Router:
    router = Router()

    POLL_ID_KEY = "POLL_ID"
    QUESTION_ID_KEY = "QUESTION_ID"

    ANSWER_CB_PREFIX = "answer_"
    ANSWER_YES = ANSWER_CB_PREFIX+"yes"
    ANSWER_NO = ANSWER_CB_PREFIX+"no"
    ANSWER_IDK = ANSWER_CB_PREFIX+"idk"


    async def _send_next_question_invite(message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        question_id = state_data.get(QUESTION_ID_KEY)
        poll_id = state_data.get(POLL_ID_KEY)
        poll = services.poll.get_poll(poll_id)
        if not poll:
            await message.answer("К сожалению, данный опрос больше не доступен.")
            return
        if question_id == len(poll.poll.questions)-1:
            await message.answer("Спасибо за участие в опросе")
            await state.clear()
            return

        buttons = [[types.InlineKeyboardButton(text=text, callback_data=cb)
                    for text, cb in [("Да", ANSWER_YES), ("Нет", ANSWER_NO), ("Не знаю", ANSWER_IDK)]]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(poll.poll.questions[question_id].text, reply_markup=keyboard)

        question_id += 1
        await state.update_data({QUESTION_ID_KEY: question_id})


    @router.callback_query(filters.Text(startswith=ACCEPT_POLL_CB_PREFIX))
    async def accept_poll_callback(query: types.CallbackQuery, state: FSMContext):
        await query.message.delete_reply_markup()
        await query.answer()

        poll_id = query.data.removeprefix(ACCEPT_POLL_CB_PREFIX)
        await state.set_state(PollAnswering.answering_question)
        await state.set_data({POLL_ID_KEY: poll_id, QUESTION_ID_KEY: 0})

        await _send_next_question_invite(query.message, state)


    @router.callback_query(filters.Text(startswith=ANSWER_CB_PREFIX), filters.StateFilter(PollAnswering.answering_question))
    async def answer_question_callback(query: types.CallbackQuery, state: FSMContext):
        await query.message.delete_reply_markup()
        await query.answer()

        answer = query.data.removeprefix(ANSWER_CB_PREFIX)
        await query.message.edit_text(query.message.text + '\nВаш ответ: ' + answer) # TODO: pretty print the answer

        await _send_next_question_invite(query.message, state)



    return router


# TODO: replace set_data with update_data everywhere
