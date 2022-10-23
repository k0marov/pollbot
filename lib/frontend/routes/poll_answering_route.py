import dataclasses
from typing import Callable, Coroutine, Any, Awaitable

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

@dataclasses.dataclass
class QuestionData:
    text: str
    poll_id: str
    question_id: int

# TODO: maybe just move this to the poll_sending_route to get rid of the typedef complexity
PollQuestionSender = Callable[[str, QuestionData], Awaitable[None]]
"""async function that sends a message with a poll question to the given chat id"""

def poll_question_sender_factory(bot: aiogram.Bot) -> PollQuestionSender:
    async def question_sender(chat_id: str, q: QuestionData) -> None:
        answers = [AnswerCB(answer=answer, poll_id=q.poll_id, question_id=q.question_id)
                   for answer in [Answer.YES, Answer.NO, Answer.IDK]]
        builder = InlineKeyboardBuilder()
        for cb in answers: builder.button(text=Texts.ANSWER(cb.answer), callback_data=cb)
        await bot.send_message(chat_id, q.text, reply_markup=builder.as_markup())

    return question_sender

def poll_answering_route(services: Services) -> Router:
    router = Router()

    @router.callback_query(AnswerCB.filter())
    async def answer_question_callback(query: types.CallbackQuery, callback_data: AnswerCB):
        await query.message.delete_reply_markup()
        await query.answer()

        poll_id = callback_data.poll_id
        poll = services.poll.get_poll(poll_id)
        if not poll: return await query.message.answer(Texts.NO_POLL)
        services.stats.record_answer(poll_id, callback_data.question_id, callback_data.answer, len(poll.questions))
        await query.message.edit_text(query.message.text + Texts.YOUR_ANSWER(callback_data.answer))

    return router
