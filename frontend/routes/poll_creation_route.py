import aiogram.exceptions
from aiogram import Router, filters
from aiogram.fsm.context import FSMContext
from aiogram.fsm import state
from aiogram import types

from backend.services.poll_service import Question, Poll
from frontend.bot import Services

# TODO: add the admin checks

class PollCreation(state.StatesGroup):
    entering_title = state.State()
    entering_question = state.State()

def poll_creation_route(services: Services) -> Router:
    router = Router()

    POLL_KEY = "poll"
    CANCEL_CB_DATA = "cancel"
    STOP_CB_DATA = "stop"

    @router.message(filters.Command("create_poll"))
    async def create_poll(message: types.Message, state: FSMContext):
        await message.answer("Введите название для нового опроса: ")
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
        print(state_data)
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
        await query.message.answer("Создание опроса отменено")
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
        await query.message.answer("Опрос успешно создан")

    async def _base_send_question_invite(message: types.Message, questions_len: int):
        buttons = [
            [types.InlineKeyboardButton(text="Закончить добавление", callback_data=STOP_CB_DATA) if questions_len else
             types.InlineKeyboardButton(text="Отменить", callback_data=CANCEL_CB_DATA)],
        ]
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
        await message.answer("Пожалуйста, введите название вопроса №" + str(questions_len+1), reply_markup=keyboard)

    return router


