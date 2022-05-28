from aiogram import types
from loguru import logger

from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, MediaGroup
from aiogram.utils.emoji import emojize

from another.request_to_API import get_works_categories, get_works_list, get_detail_info_about_work
from keyboards.callback_data_bot import callback_for_inline
from keyboards.inline_keyboard import formation_keyboard
from keyboards.reply_keyboard import CAT_LST_DTL_KEYBRD
from settings.config import KEYBOARD, DP, DOMAIN_NAME


@logger.catch
async def works_categories_inline_keybrd(message: types.Message):
    '''Раздел категорий работ.'''
    # отправляет реплай клавиатуру для навигации по меню бота
    await message.answer(f'{emojize(":robot:")} Вы в разделе КАТЕГОРИИ РАБОТ\n'
                         f'Работаю с сервером...{emojize(":desktop_computer:")}', reply_markup=CAT_LST_DTL_KEYBRD)
    # выполняем запрос к АПИ БД
    response = await get_works_categories()
    # формируем инлайн клавиатуру
    inline_keybrd = formation_keyboard(response, step_id=1)
    # отправляем пользователю сообщение и инлайн клавиатуру
    await message.answer('Выберите одну из категорий под сообщением.', reply_markup=inline_keybrd)


@logger.catch
async def all_works_categories_inline_keybrd(message: types.Message):
    '''Раздел список всех выполненных работ'''

    # отправляет реплай клавиатуру для навигации по меню бота
    await message.answer(f'{emojize(":robot:")}Произвожу запрос на получение списка выполненных работ\n'
                              f'Работаю с сервером...{emojize(":desktop_computer:")}', reply_markup=CAT_LST_DTL_KEYBRD)
    response = await get_works_list()
    inline_keybrd = formation_keyboard(response, step_id=2)
    await message.answer('Список выполненных работ ниже, нажимайте на любую.', reply_markup=inline_keybrd)


@logger.catch
async def works_list_by_category(call: CallbackQuery, callback_data: dict):
    '''Список выполненных работ по выбранной категории.'''

    await call.answer(cache_time=5)
    # отправляет реплай клавиатуру для навигации по меню бота
    await call.message.answer(f'{emojize(":robot:")}Произвожу поиск выполненных работ для выбранной категории\n'
                              f'Работаю с сервером...{emojize(":desktop_computer:")}', reply_markup=CAT_LST_DTL_KEYBRD)
    response = await get_works_list(category_id=callback_data["id"])
    inline_keybrd = formation_keyboard(response, step_id=2)
    await call.message.answer('Список выполненных работ ниже, нажимайте на любую.', reply_markup=inline_keybrd)


@logger.catch
async def detail_works_list_by_category(call: CallbackQuery, callback_data: dict):
    '''Реакция на нажатие кнопки отмены'''
    await call.answer(cache_time=5)
    await call.message.answer(f'{emojize(":robot:")}Запрашиваю информацию по данной работе\n'
                              f'Работаю с сервером...{emojize(":desktop_computer:")}', reply_markup=CAT_LST_DTL_KEYBRD)
    response = await get_detail_info_about_work(work_id=callback_data['id'])
    about_work_text = f'Название работы: {response[0]["work_title"]}\n' \
                      f'Цена работы: {int(response[0]["result_price"])} руб.\n' \
                      f'Дата выполнения: {response[0]["date_of_completion"]}\n' \
                      f'\nОписание работы:\n{response[0]["work_description"]}'
    await call.message.answer(about_work_text)

    # создаём альбом для медиа группы
    album = MediaGroup()
    # итерируемся по всем медиа объектам для данной работы
    for i_elem in response[1]:
        # если формат соответствует картинке
        if i_elem['media_file'].endswith('.jpg') or i_elem['media_file'].endswith('.png'):
            # берём ссылку на картинку
            photo_url = ''.join([DOMAIN_NAME, i_elem['media_file']])
            # await call.message.answer(photo_url)  # эту хуйню удалить, как будет сервер с АПИ
            # вставляем в альбом
            album.attach_photo(photo_url)
        # если формат соответствует видео
        elif i_elem['media_file'].endswith('.mp4'):
            video_url = ''.join([DOMAIN_NAME, i_elem['media_file']])
            # await call.message.answer(video_url)  # эту хуйню удалить, как будет сервер с АПИ
            album.attach_video(video_url)
    await call.message.answer_media_group(media=album)


@logger.catch
def register_step_by_step_handlers():
    '''Функция регистрации обработчиков для клавиатуры в инлайн режиме'''

    DP.register_message_handler(works_categories_inline_keybrd, Text(equals=[KEYBOARD['CATEGORY']]))
    DP.register_message_handler(all_works_categories_inline_keybrd, Text(equals=[KEYBOARD['WORK_LIST']]))
    # для регистрации тут используем register_callback_query_handler
    # какого-то хрена параметры колбэка считываются как строки, даже если они были переданы как int, bool
    DP.register_callback_query_handler(works_list_by_category, callback_for_inline.filter(step='1'))
    DP.register_callback_query_handler(detail_works_list_by_category, callback_for_inline.filter(step='2'))

