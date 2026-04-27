from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def main_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Проверить баланс', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Помощь', color=VkKeyboardColor.SECONDARY)
    return keyboard.get_keyboard()


def second_keyboard():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Ответить', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Отказаться', color=VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def send_message(vk, peer_id, text, keyboard_idx=0):
    keybords = [main_keyboard(), second_keyboard()]
    params = {
        'peer_id': peer_id,
        'message': text,
        'random_id': get_random_id(),
        'keyboard': keybords[keyboard_idx]
    }

    vk.messages.send(**params)
