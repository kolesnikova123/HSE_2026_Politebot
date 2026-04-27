from vk_helper import main_keyboard, second_keyboard, send_message
from vk_api.utils import get_random_id
from ai import OpenRouterClient
import requests
import os


HELP_TEXT = """
/help - эта справка
/balanse - проверить карму
/opros - сделать рассылку опроса (только для учителя)
/answer - ответить на опрос
/refuse - отказаться от ответа
/cat - посмотреть на котика
"""

# Инициализация клиента ИИ
ai_client = OpenRouterClient(api_key=str(os.getenv("OPENROUTER_API_KEY")),
                             model="qwen/qwen3.5-flash-02-23",
                             default_system_prompt=""
                             )


def get_random_cat_image_url():
    """
    Запрашивает у API thecatapi.com ссылку на случайную картинку котика.
    Возвращает строку с URL или текст ошибки.
    """
    try:
        # Делаем запрос к API.
        # User-Agent нужен, чтобы нас не заблокировали как бота.
        headers = {'x-api-key': 'DEMO-API-KEY'}  # Ключ для демо-режима
        response = requests.get(
            'https://api.thecatapi.com/v1/images/search', headers=headers)

        # Проверяем, успешно ли прошел запрос (код 200)
        if response.status_code == 200:
            # Ответ приходит в формате JSON (текст). Преобразуем его в словарь Python.
            data = response.json()
            # Так как мы запрашиваем массив, берем первый элемент [0] и достаем ссылку 'url'
            return data[0]['url']
        else:
            return f"Ошибка при получении котика (код {response.status_code})."

    except Exception:
        # Если что-то пошло не так (например, нет интернета)
        return "Не удалось связаться с сервером котиков."


# Глобальный список для хранения user_id
connected_users: set[str] = set()


def handle(user_id, text, vk_api_obj, admin_id):
    global connected_users

    text = text.strip()

    # Сохраняем пользователя, если он начал диалог
    if (text.lower().startswith("начать") or text.lower().startswith("/start")):
        connected_users.add(str(user_id))
        print(connected_users)
        return "В данный момент нет активных опросов."

    # Помощь
    if text.lower().startswith("/help") or text.lower().startswith("помощь"):
        return HELP_TEXT

    # Баланс
    if text.lower().startswith("/balanse") or "баланс" in text.lower():
        return "Ваша карма сейчас: 10 баллов."

    # Ответить на опрос
    if text.lower().startswith("/answer") or "ответить" in text.lower():
        # Если хотите чтоб модель
        # if ai_client.is_toxic(text[8:].strip()):
        #     return "Ваше сообщение содержит токсичный контент. Пожалуйста, будьте вежливы."
        # else:
        #     return "Вы великолепны! Напишите '/cat' и посмотрите на котика."

        return "Вы великолепны! Напишите '/cat' и посмотрите на котика."

    # Отказаться от опроса
    if text.lower().startswith("/refuse") or "отказаться" in text.lower():
        return "Спасибо за участие! Вы отказались от опроса."

    # Рассылка опроса
    if text.lower().startswith("/opros"):
        # Проверка прав (только для админа - учителя)
        if str(user_id) == str(admin_id):
            message = text[7:].strip()  # Текст после /opros

            if not message:
                return "Пожалуйста, укажите текст для рассылки после команды /opros"

            # Рассылка всем подключённым пользователям
            for uid in connected_users:
                try:
                    send_message(vk_api_obj, uid, message, keyboard_idx=1)
                except Exception as e:
                    print(f"Не удалось отправить сообщение {uid}: {e}")

            return "Рассылка завершена."
        else:
            return "У вас нет прав на отправку опроса."

    # Котик/
    if text.lower() == '/cat' or text.lower() == 'котик':
        cat_image_url = get_random_cat_image_url()
        message = f"Посмотрите на этого котика!\n{cat_image_url}"
        return message

    return "К сожалению, я вас не понимаю. Для получения списка команд - отправьте '/help.'"
