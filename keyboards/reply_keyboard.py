from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from settings.config import KEYBOARD


'''Клавиатура главного меню'''
MAIN_MENU = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text=KEYBOARD['APPLICATION'])
        ],
        [
            KeyboardButton(text=KEYBOARD['CATEGORY']),
            KeyboardButton(text=KEYBOARD['CONTACTS']),
        ],
        [
            KeyboardButton(text=KEYBOARD['WORK_LIST'])
        ],
    ],
    resize_keyboard=True    # это, чтобы клавиатура не занимала пол экрана
)

'''Клавиатура для разделов: категории, наши работы'''
CAT_LST_DTL_KEYBRD = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text=KEYBOARD['APPLICATION'])
        ],
        [
            KeyboardButton(text=KEYBOARD['CONTACTS']),
        ],
        [
            KeyboardButton(text=KEYBOARD['HEAD_PAGE'])
        ],
    ],
    resize_keyboard=True    # это, чтобы клавиатура не занимала пол экрана
)