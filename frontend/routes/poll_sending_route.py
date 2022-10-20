from aiogram import Router, filters, types

from backend.services.services import Services
from frontend.routes import poll_answering_route


# TODO: maybe move poll saving from a db to the aiogram's state or some other built-in feature.
#  This will make it easier to implement every admin having its own poll list.

def poll_sending_route(services: Services, send_poll_invite: poll_answering_route.PollInviteSender) -> Router:
    router = Router()

    @router.message(filters.Command("send_poll"))
    async def admin_send_poll_handler(message: types.Message):
        id = message.text.removeprefix("/send_poll").strip() # TODO: proper way of sending polls (without bothering the user with using the ids)
        poll = services.poll.get_poll(id)
        if not poll: return await message.answer("Опроса с таким id не найдено.")
        all_users = [user for user in services.user.get_all_users() if user != str(message.chat.id)]
        for user in all_users:
            await send_poll_invite(user, poll)

        await message.answer("Приглашение поучавствовать в опросе было отправлено в %d чатов" % len(all_users))

    return router
