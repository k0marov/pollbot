from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from telegram import InlineKeyboardMarkup

from frontend.bot import Services

class PollCreation(StatesGroup):
    entering_question = State()




def poll_creation_route(services: Services) -> Router:
    router = Router()

    QUESTIONS_KEY = "questions"
    CANCEL_CB_DATA = "cancel"
    STOP_CB_DATA = "stop"

    async def _base_send_question_invite(message: Message, state: FSMContext):
        current_state = await state.get_data()
        questions = current_state.get(QUESTIONS_KEY, [])
        buttons = [
            [InlineKeyboardButton(text="Закончить добавление", callback_data=STOP_CB_DATA) if questions else
             InlineKeyboardButton(text="Отменить", callback_data=CANCEL_CB_DATA)],
        ]
        keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Пожалуйста, введите название вопроса №" + str(len(questions) + 1), reply_markup=keyboard)

    @router.message(Command("create_poll"))
    async def create_poll(message: Message, state: FSMContext):
        await _base_send_question_invite(message, state)
        await state.set_state(PollCreation.entering_question)

    @router.message(PollCreation.entering_question)
    async def enter_question(message: Message, state: FSMContext):
        current_state = await state.get_data()
        questions = current_state.get(QUESTIONS_KEY)
        new_questions = [questions] + [message.text]
        await state.update_data(QUESTIONS_KEY=new_questions)
        await _base_send_question_invite(message, state)


    # TODO: change all imports to use types module

    @router.callback_query(Text(text=CANCEL_CB_DATA))
    async def cancel_callback(query: CallbackQuery, state: FSMContext):
        print("here")
        await query.message.delete_reply_markup()
        await query.message.answer("Создание опроса отменено")
        await state.clear()




    return router


