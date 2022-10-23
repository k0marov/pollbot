import asyncio
from typing import Awaitable

import typing
from aiogram import Router, filters, types
from aiogram.filters import callback_data
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lib.backend.services.poll import PollEntity, Poll
from lib.backend.services.services import Services
from lib.frontend.design.texts import Texts
from lib.frontend.middlewares.admin_middleware import AdminCheckMiddleware
from lib.frontend.routes import poll_answering_route


# TODO: maybe move poll saving from a db to the aiogram's state or some other built-in feature.
#  This will make it easier to implement every admin having its own poll list.
from lib.frontend.routes.poll_answering_route import QuestionData


class SendQuestionCB(callback_data.CallbackData, prefix="send_q_"):
    poll_id: str
    question_id: int

def poll_sending_route(services: Services, send_question: poll_answering_route.PollQuestionSender, admin_mw: AdminCheckMiddleware) -> Router:
    router = Router()
    router.message.middleware(admin_mw.msg)
    router.callback_query.middleware(admin_mw.cb)

    @router.message(filters.Command("send_poll"))
    async def admin_send_poll_handler(message: types.Message):
        # TODO: remove code duplication with poll_stats_route
        polls = services.poll.get_all_polls()
        builder = InlineKeyboardBuilder()
        for e in polls:
            builder.button(text=e.poll.title, callback_data=SendQuestionCB(poll_id=e.id, question_id=0))
        await message.answer(Texts.CHOOSE_POLL, reply_markup=builder.as_markup())


    async def _send_question_to_all_users(poll: Poll, q: SendQuestionCB, all_users: typing.List[str]):
        # TODO: place a timeout here to escape the 429 Too Many Requests error
        return await asyncio.gather(*[
            send_question(user, QuestionData(
                text=poll.questions[q.question_id].text,
                poll_id=q.poll_id,
                question_id=q.question_id,
            ))
            for user in all_users
        ])


    @router.callback_query(SendQuestionCB.filter())
    async def send_question_handler(query: types.CallbackQuery, callback_data: SendQuestionCB):
        cb = callback_data
        poll = services.poll.get_poll(cb.poll_id)
        if not poll: return await query.message.answer(Texts.NO_POLL)
        all_users = [user for user in services.user.get_all_users() if user != str(query.message.chat.id)]
        await _send_question_to_all_users(poll, cb, all_users)

        await query.answer()
        await query.message.delete_reply_markup()
        if cb.question_id == len(poll.questions) - 1:
            await query.message.edit_text(f"Вопрос №{cb.question_id+1} отправлен всем пользователям") # TODO remove code duplication
        else:
            next_cb = SendQuestionCB(poll_id=cb.poll_id, question_id=cb.question_id+1)
            builder = InlineKeyboardBuilder()
            builder.button(text="Следующий вопрос", callback_data=next_cb)
            await query.message.edit_text(f"Вопрос №{cb.question_id+1} отправлен всем пользователям", reply_markup=builder.as_markup())


    return router
