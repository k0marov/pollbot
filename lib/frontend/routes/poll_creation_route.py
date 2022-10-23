import aiogram.exceptions
from aiogram import Router, filters
from aiogram.fsm.context import FSMContext
from aiogram.fsm import state
from aiogram import types

from lib.backend.services.poll import Question, Poll
from lib.frontend.bot import Services

from lib.frontend.design.texts import Texts
from lib.frontend.middlewares.admin_middleware import AdminCheckMiddleware


class PollCreation(state.StatesGroup):
    entering_title = state.State()
    entering_question = state.State()

def poll_creation_route(services: Services, admin_mw: AdminCheckMiddleware) -> Router:
    router = Router()
    router.message.middleware(admin_mw.msg)
    router.callback_query.middleware(admin_mw.cb)

    POLL_KEY = "poll"
    CANCEL_CB_DATA = "cancel"
    STOP_CB_DATA = "stop"

    @router.message(filters.Command("create_poll"))
    async def create_poll(message: types.Message, state: FSMContext):
        await message.answer(Texts.ENTER_TITLE)
        await state.set_state(PollCreation.entering_title)

    @router.message(PollCreation.entering_title) # TODO: handle the cases when users sends messages without text
    async def title_entered(message: types.Message, state: FSMContext):
        title = message.text
        await state.update_data({POLL_KEY: Poll(title, [])})
        await state.set_state(PollCreation.entering_question)
        await _base_send_question_invite(message, 0)

    @router.message(PollCreation.entering_question)
    async def question_entered(message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        poll = state_data.get(POLL_KEY)
        if not poll:
            raise aiogram.exceptions.TelegramNotFound
        poll.questions.append(Question(text=message.text))
        await state.update_data({POLL_KEY: poll})
        await _base_send_question_invite(message, len(poll.questions))

    @router.callback_query(filters.Text(text=CANCEL_CB_DATA))
    async def cancel_callback(query: types.CallbackQuery, state: FSMContext):
        await query.message.delete_reply_markup()
        await state.clear()
        await query.message.answer(Texts.CREATION_CANCELLED)
        await query.answer()

    @router.callback_query(filters.Text(text=STOP_CB_DATA))
    async def stop_callback(query: types.CallbackQuery, state: FSMContext):
        await query.answer()
        await query.message.delete_reply_markup()

        state_data = await state.get_data()
        poll = state_data.get(POLL_KEY)
        if not poll: return
        services.poll.create_poll(poll)
        await state.clear()
        await query.message.answer(Texts.POLL_CREATED)

    async def _base_send_question_invite(message: types.Message, questions_len: int):
        buttons = [
            [types.InlineKeyboardButton(text=Texts.STOP_ADDING, callback_data=STOP_CB_DATA) if questions_len else
             types.InlineKeyboardButton(text=Texts.CANCEL, callback_data=CANCEL_CB_DATA)],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer(Texts.ENTER_QUESTION(questions_len+1), reply_markup=keyboard)

    return router


