import os
import random
from vk_api import VkApi
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from dotenv import load_dotenv

from handle import handle
from vk_helper import send_message
from ai import OpenRouterClient


load_dotenv()
group_id = os.getenv("GROUP_ID")
group_token = os.getenv("GROUP_TOKEN")
admin_id = os.getenv("ADMIN_ID")


# Инициализация клиента ИИ
ai_client = OpenRouterClient(api_key=str(os.getenv("OPENROUTER_API_KEY")),
                             model="qwen/qwen3.5-flash-02-23",
                             default_system_prompt=""
                             )


def run_bot() -> None:
    vk_session = VkApi(token=group_token)
    vk = vk_session.get_api()
    longpoll = VkBotLongPoll(vk_session, group_id, 25)

    print("Все ок!")

    for event in longpoll.listen():

        # 1. Проверяем, пришло ли новое текстовое сообщение
        if event.type == VkBotEventType.MESSAGE_NEW:
            user_id = event.message.peer_id
            text = event.message.text

            res = handle(user_id, text, vk, admin_id)

            if res:
                send_message(vk, user_id, res)

        # 2. Проверяем, нажал ли пользователь кнопку
        elif event.type == VkBotEventType.MESSAGE_EVENT:
            # Объект события содержит всю нужную информацию
            user_id = event.object.peer_id
            payload = event.object.payload  # Это словарь, который мы передали в кнопке

            print(
                f"Нажата кнопка! От пользователя {user_id}. Данные: {payload}")

            # Проверяем, какая именно кнопка была нажата
            if payload and payload.get('type') == 'Отказаться':
                response_text = "Спасибо за участие! Вы отказались от опроса."
                send_message(vk, user_id, response_text, keyboard_idx=0)
                # Уведомляем админа (если нужно)
                send_message(vk, admin_id,
                             f"User {user_id} отказался от опроса.")

            elif payload and payload.get('type') == 'Ответить':
                send_message(vk, user_id,
                             "Вы нажали 'Ответить'. Введите ваш ответ:",
                             keyboard_idx=None
                             )
                # ... здесь нужно запросить ввод текста и отправить его ИИшке...
                # Проверка на токсичность (работает с каким-то текстом, но не с пользовательским)
                test_messages = [
                    "Привет, как дела?",
                    "Ты полный идиот, удались!",
                    "Мне не нравится твой ответ",
                    "Убью тебя, урод",
                ]
                random_message = random.choice(test_messages)
                if ai_client.is_toxic(random_message):
                    send_message(vk, user_id,
                                 "Ваше сообщение содержит токсичный контент. Пожалуйста, будьте вежливы."
                                 )
                else:
                    send_message(vk, user_id,
                                 "Вы великолепны! Напишите '/cat' и посмотрите на котика."
                                 )


run_bot()
