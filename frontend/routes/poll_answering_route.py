import asyncio
from typing import Callable, Coroutine, Any

import aiogram
from aiogram import types, Router, filters
from aiogram.filters import callback_data
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend.services import poll
from backend.services.poll import Answer
from backend.services.services import Services

# TODO: move all of the text literals to a separate module as constants


class AnswerCB(callback_data.CallbackData, prefix="answer"):
    answer: Answer
    poll_id: str
    question_id: int

# TODO: move keyboards to a separate module

# TODO: maybe just move this to the poll_sending_route to get rid of the typedef complexity
PollInviteSender = Callable[[str, poll.PollEntity], Coroutine[Any, Any, None]]
"""async function that sends a message with a poll invitation to the given chat id"""

ACCEPT_POLL_CB_PREFIX = "accept_poll_"

def poll_invite_sender_factory(bot: aiogram.Bot) -> PollInviteSender:
    async def invite_sender(chat_id: str, poll: poll.PollEntity) -> None:
        print("inviting user %s" % chat_id)
        cb_data = ACCEPT_POLL_CB_PREFIX + poll.id
        buttons = [[aiogram.types.InlineKeyboardButton(text="OK", callback_data=cb_data)]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        text = "Пожалуйста, поучавствуйте в опросе: " + poll.poll.title
        await bot.send_message(chat_id, text, reply_markup=keyboard)

    return invite_sender

def poll_answering_route(services: Services) -> Router:
    router = Router()

    async def _send_next_question_invite(message: types.Message, poll_id: str, question_id: int):
        poll = services.poll.get_poll(poll_id)
        if not poll:
            await message.answer("К сожалению, данный опрос больше не доступен.")
            return
        if question_id > len(poll.questions)-1:
            await message.answer("Спасибо за участие в опросе")
            return

        answers = [(answer, AnswerCB(answer=answer, poll_id=poll_id, question_id=question_id))
                   for answer in [Answer.YES, Answer.NO, Answer.IDK]]
        builder = InlineKeyboardBuilder()
        for text, cb in answers: builder.button(text=text, callback_data=cb)
        await message.answer(poll.questions[question_id].text, reply_markup=builder.as_markup())


    @router.callback_query(filters.Text(startswith=ACCEPT_POLL_CB_PREFIX))
    async def accept_poll_callback(query: types.CallbackQuery):
        await query.message.delete_reply_markup()
        await query.answer()

        poll_id = query.data.removeprefix(ACCEPT_POLL_CB_PREFIX)

        await _send_next_question_invite(query.message, poll_id, question_id=0)

    @router.callback_query(AnswerCB.filter())
    async def answer_question_callback(query: types.CallbackQuery, callback_data: AnswerCB):
        await query.message.delete_reply_markup()
        await query.answer()

        services.poll.record_answer(callback_data.poll_id, callback_data.question_id, callback_data.answer)
        await query.message.edit_text(query.message.text + '\nВаш ответ: ' + callback_data.answer) # TODO: pretty print the answer

        await _send_next_question_invite(query.message, callback_data.poll_id, callback_data.question_id+1)



    return router


# TODO: replace set_data with update_data everywhere
