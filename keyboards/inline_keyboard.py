from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callback_data_bot import callback_for_inline, callback_for_cancel
from settings.config import KEYBOARD


def formation_keyboard(response_data: list, step_id: int):
    '''
    Функция для формирования инлайн клавиатуры.
    Принимает ответ - результат запроса к API БД в виде списка кортежей (id, name).
    Возвращает клавиатуру с инлайн кнопками.
    '''
    # создаём клавиатуру
    inline_keyboard = InlineKeyboardMarkup(row_width=1)

    for i_resp_data in response_data:
        # создаём кнопку
        inline_button = InlineKeyboardButton(
            text=f'✅ {i_resp_data[1]}',
            callback_data=callback_for_inline.new(
                id=i_resp_data[0],
                step=step_id
            )
        )
        # вставляем кнопку в клавиатуру
        inline_keyboard.insert(inline_button)

    return inline_keyboard


CANCEL_INLINE_KEYBOARD = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(
            text=KEYBOARD['CANCEL_SEND'],
            callback_data=callback_for_cancel.new(cancel=True)
        )
    ],
])
