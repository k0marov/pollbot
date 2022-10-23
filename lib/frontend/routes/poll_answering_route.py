from typing import Callable, Coroutine, Any

import aiogram
from aiogram import types, Router, filters
from aiogram.filters import callback_data
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lib.backend.services import poll
from lib.backend.services.poll import PollEntity
from lib.backend.services.stats import Answer
from lib.backend.services.services import Services

from lib.frontend.design.texts import Texts


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
        cb_data = ACCEPT_POLL_CB_PREFIX + poll.id
        buttons = [[aiogram.types.InlineKeyboardButton(text=Texts.PARTICIPATE_OK, callback_data=cb_data)]]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await bot.send_message(chat_id, Texts.POLL_INVITE(poll.poll), reply_markup=keyboard)

    return invite_sender

def poll_answering_route(services: Services) -> Router:
    router = Router()

    async def _send_next_question_invite(message: types.Message, poll: PollEntity, question_id: int):
        if question_id > len(poll.poll.questions)-1:
            await message.answer(Texts.PARTICIPATION_THANKS)
            return

        answers = [AnswerCB(answer=answer, poll_id=poll.id, question_id=question_id)
                   for answer in [Answer.YES, Answer.NO, Answer.IDK]]
        builder = InlineKeyboardBuilder()
        for cb in answers: builder.button(text=Texts.ANSWER(cb.answer), callback_data=cb)
        await message.answer(poll.poll.questions[question_id].text, reply_markup=builder.as_markup())


    @router.callback_query(filters.Text(startswith=ACCEPT_POLL_CB_PREFIX))
    async def accept_poll_callback(query: types.CallbackQuery):
        await query.message.delete_reply_markup()
        await query.answer()

        poll_id = query.data.removeprefix(ACCEPT_POLL_CB_PREFIX)
        poll = services.poll.get_poll(poll_id)
        if not poll: return await query.message.answer(Texts.NO_POLL)

        await _send_next_question_invite(query.message, PollEntity(poll_id, poll), question_id=0)

    @router.callback_query(AnswerCB.filter())
    async def answer_question_callback(query: types.CallbackQuery, callback_data: AnswerCB):
        await query.message.delete_reply_markup()
        await query.answer()

        poll_id = callback_data.poll_id
        poll = services.poll.get_poll(poll_id)
        if not poll: return await query.message.answer(Texts.NO_POLL)
        services.stats.record_answer(poll_id, callback_data.question_id, callback_data.answer, len(poll.questions))
        await query.message.edit_text(query.message.text + Texts.YOUR_ANSWER(callback_data.answer))

        await _send_next_question_invite(query.message, PollEntity(poll_id, poll), callback_data.question_id+1)



    return router
