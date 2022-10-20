from typing import List

from aiogram import Router, filters
from aiogram.fsm.context import FSMContext
from aiogram.fsm import state
from aiogram import types

from backend.services import poll_service
from backend.services.poll_service import Question
from frontend.bot import Services

# TODO: add the admin checks

class PollCreation(state.StatesGroup):
    entering_question = state.State()

def poll_creation_route(services: Services) -> Router:
    router = Router()

    QUESTIONS_KEY = "questions"
    CANCEL_CB_DATA = "cancel"
    STOP_CB_DATA = "stop"

    @router.message(filters.Command("create_poll"))
    async def create_poll(message: types.Message, state: FSMContext):
        await _base_send_question_invite(message)
        await state.set_state(PollCreation.entering_question)

    @router.message(PollCreation.entering_question)
    async def question_entered(message: types.Message, state: FSMContext):
        state_data = await state.get_data()
        questions = state_data.get(QUESTIONS_KEY, [])
        questions.append(message.text)
        await state.update_data({QUESTIONS_KEY: questions})
        await _base_send_question_invite(message, questions)

    @router.callback_query(filters.Text(text=CANCEL_CB_DATA))
    async def cancel_callback(query: types.CallbackQuery, state: FSMContext):
        await query.message.delete_reply_markup()
        await state.clear()
        await query.message.answer("Создание опроса отменено")
        await query.answer()

    @router.callback_query(filters.Text(text=STOP_CB_DATA))
    async def stop_callback(query: types.CallbackQuery, state: FSMContext):
        state_data = await state.get_data()
        questions = state_data.get(QUESTIONS_KEY, [])
        if not questions: return
        poll = poll_service.Poll(questions=[
            Question(text=text) for text in questions
        ])
        services.poll.create_poll(poll)
        await state.clear()
        await query.message.answer("Опрос успешно создан")
        await query.answer()

    async def _base_send_question_invite(message: types.Message, questions: List[str] = []):
        buttons = [
            [types.InlineKeyboardButton(text="Закончить добавление", callback_data=STOP_CB_DATA) if questions else
             types.InlineKeyboardButton(text="Отменить", callback_data=CANCEL_CB_DATA)],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        question_index = str(len(questions) + 1)
        await message.answer("Пожалуйста, введите название вопроса №" + question_index, reply_markup=keyboard)

    return router


