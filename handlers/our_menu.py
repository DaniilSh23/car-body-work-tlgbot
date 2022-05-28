from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import ReplyKeyboardRemove
from emoji import emojize

from handlers.inline_menu import example_inline_keyboard
from keyboards.reply import OUR_MENU
from settings.config import KEYBOARD


async def home_page(message: types.Message):
    '''Обработчик для общего меню бота'''
    # отвечаем пользователю и отправляем ему клавиатуру
    await message.answer('Вас приветствуют автоботы! Вам поможет авто-бот Бамблби', reply_markup=OUR_MENU)


async def reaction_on_many_button(message: types.Message):
    '''Реакция бота на нажатие кнопок вперёд или назад'''
    # reply_markup здесь убирает клавиатуру у пользователя
    await message.answer(f'Вы выбрали {message.text}', reply_markup=ReplyKeyboardRemove())


async def reaction_on_order_button(message: types.Message):
    '''Реакция бота на нажатие кнопки ✅ ЗАКАЗ'''
    await message.answer(f'Вы выбрали {message.text}', reply_markup=ReplyKeyboardRemove())


async def reaction_on_applay_button(message: types.Message):
    '''Реакция бота на нажатие кнопки ✅ Оформить заказ'''
    await message.answer(f'Вы выбрали {message.text}', reply_markup=ReplyKeyboardRemove())


def register_our_menu(dp: Dispatcher):
    '''Функция для регистрации обработчиков'''

    dp.register_message_handler(home_page, Command(['start', 'home',]))
    dp.register_message_handler(home_page, Text(equals=[KEYBOARD['HEAD_PAGE']]))
    # прописываем в регистрации встроенный фильтр Text, которому передаём точное совпадение со строками
    dp.register_message_handler(reaction_on_many_button, Text(equals=['◀️', '▶️']))
    dp.register_message_handler(reaction_on_order_button, Text(equals=['✅ ЗАКАЗ']))
    dp.register_message_handler(reaction_on_applay_button, Text(equals=['✅ Оформить заказ']))
    dp.register_message_handler(example_inline_keyboard, Text(equals='INLINE_KEYBOARD'))



