from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery, ReplyKeyboardRemove

from keyboards.callback_data_example import callback_for_example_inline
from keyboards.inline import EXAMPLE_INLINE_KEYBOARD, link_keyboard
from keyboards.reply import TO_HOME_PAGE


async def example_inline_keyboard(message: types.Message):
    '''Пример работы инлайн клавиатуры'''

    # убираем клавиатуру с общим меню
    await message.answer(f'Вы выбрали {message.text}', reply_markup=ReplyKeyboardRemove())
    await message.answer('Вот пример работы инлайн клавиатуры', reply_markup=EXAMPLE_INLINE_KEYBOARD)


async def inline_button_icecream(call: CallbackQuery, callback_data: dict):
    '''Реакция на нажатие кнопки ICE CREAM'''

    await call.answer(cache_time=5)
    await call.message.answer(f'Данные просто {call.data}')
    await call.message.answer(f'Данные из словаря {callback_data}')


async def inline_button_settings(call: CallbackQuery, callback_data: dict):
    '''Реакция на нажатие кнопки настроек'''

    await call.answer(cache_time=10)
    await call.message.answer(f'Данные просто {call.data}')
    await call.message.answer(f'Данные из словаря {callback_data}')


async def inline_button_cancel(call: CallbackQuery, callback_data: dict):
    '''Реакция на нажатие кнопки отмены'''

    # выводим сообщение в виде алерт окна
    await call.answer(f'Вы что-то отменили', show_alert=True)
    # убираем старую клавиатуру и добавляем другую
    await call.message.edit_reply_markup()
    await call.message.answer(text='Вы можете перейти на главное меню', reply_markup=TO_HOME_PAGE)


async def inline_keyboard_with_link(call: CallbackQuery, callback_data: dict):
    '''Вызываем инлайн клавиатуру с ссылкой'''

    await call.answer(cache_time=15)
    await call.message.answer(text='а вот и клавиатура с какой-то ссылочкой подъехала', reply_markup=link_keyboard)


def register_inline_mode(dp: Dispatcher):
    '''Функция регистрации обработчиков для клавиатуры в инлайн режиме'''

    # для регистрации тут используем register_callback_query_handler
    dp.register_callback_query_handler(inline_button_icecream, callback_for_example_inline.filter(second='мороженое'))
    dp.register_callback_query_handler(inline_button_settings, callback_for_example_inline.filter(second='настройки'))
    dp.register_callback_query_handler(inline_button_cancel, callback_for_example_inline.filter(second='Галя_отмена'))
    dp.register_callback_query_handler(inline_keyboard_with_link, callback_for_example_inline.filter(second='link'))
