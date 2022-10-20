import aiogram
from aiogram import Router, filters, types

from backend.services.services import Services


def poll_sending_route(bot: aiogram.Bot, services: Services) -> Router:
    router = Router()

    # @router.message(filters.Command("send_poll"))
    # async def admin_send_poll(message: types.Message):
    #     id = message.text.removeprefx("send_poll").strip()
    #     poll = services.poll.get_poll(id)
    #     all_users = services.user.get_all_users()
    #     for user in all_users:
    #     pass



    return router
