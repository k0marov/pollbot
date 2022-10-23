from lib.backend.services.poll import Poll

from lib.backend.services.stats import PollStats, Answer


class Texts:
    GREET = \
"""
Привет, я - бот для проведения анонимных опросов. 
Благодаря мне вы можете получать полностью анонимные опросы. 
Спасибо за регистрацию!
"""
    HELP = \
"""
Список команд: 
/admin_login <пароль> - получить права админа
Команды для админов: 
/create_poll - создание нового опроса 
/send_poll - рассылка опроса 
/stats - получение статистики по опросу 
"""

    NEED_ADMIN_RIGHTS = "Чтобы выполнить это действие, нужно быть админом. Введите /admin_login"
    ADMIN_LOGIN_SUCCESS = "Вы успешно зарегистрировались в качестве админа."
    ADMIN_LOGIN_FAIL = "Ошибка - неверный пароль"
    CHOOSE_POLL = "Выберите опрос:"
    NO_STATS = "Для этого опроса пока нет статистики."
    NO_POLL = "Опроса с таким id не найдено."
    ENTER_TITLE = "Введите название для нового опроса: "
    CREATION_CANCELLED = "Создание опроса отменено."
    POLL_CREATED = "Опрос успешно создан."
    STOP_ADDING = "Закончить добавление"
    CANCEL = "Отменить"
    PARTICIPATION_THANKS = "Спасибо за участие в опросе"
    PARTICIPATE_OK = "OK"
    def CHOSEN_POLL(poll: Poll) -> str:
       return f'\nВыбран опрос {poll.title}'
    def STATS(poll: Poll, stats: PollStats) -> str:
        text = f"Статистика для опроса \"{poll.title}\"\n"
        for i, qstats in enumerate(stats.question_stats):
            text += \
f"""
{poll.questions[i].text}:
    "Да": {qstats.yes}
    "No": {qstats.no}
    "Не знаю": {qstats.idk}\n
"""
        return text
    def INVITATIONS_REPORT(invites: int) -> str:
        return f"Приглашение поучавствовать в опросе было отправлено в {invites} чат" + ("ов" if invites % 10 > 1 else "")
    def ENTER_QUESTION(index: int) -> str:
        return f"Пожалуйста, введите название вопроса №{index}"
    def POLL_INVITE(poll: Poll) -> str:
        return f"Пожалуйста, поучавствуйте в опросе: \"{poll.title}\""
    def YOUR_ANSWER(answer: Answer) -> str:
        return f'\nВаш ответ: {Texts.ANSWER(answer)}'
    def ANSWER(a: Answer) -> str:
        if a == Answer.YES:
            return "Да"
        elif a == Answer.NO:
            return "Нет"
        elif a == Answer.IDK:
            return "Не знаю"








