from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text, ContentTypeFilter
from aiogram.types import CallbackQuery, ReplyKeyboardRemove
from emoji import emojize
from loguru import logger

from another.request_to_API import post_create_new_application
from another.states import ApplicationSendStates
from keyboards.callback_data_bot import callback_for_cancel
from keyboards.inline_keyboard import CANCEL_INLINE_KEYBOARD
from keyboards.reply_keyboard import MAIN_MENU, CAT_LST_DTL_KEYBRD
from settings.config import KEYBOARD, ADMIN_ID, BOT, DP


@logger.catch
async def start_message(message: types.Message):
    '''Обработчик для команды /start'''

    # отвечаем пользователю и отправляем ему клавиатуру
    await message.answer(f'{emojize(":robot:")}Привет, я бот-помощник в сфере услуг ремонта кузова авто{emojize(":racing_car:")}.\n\n'
                         '▶Вы можете оставить заявку, чтобы мастер смог предварительно оценить сложность работы.\n'
                         '▶Узнать о видах работ, которые мы выполняем лучше остальных.\n'
                         '▶Или посмотреть какие работы мы уже выполняли, чтобы понять, '
                         'что мы действительно сделаем это лучше других.\n'
                         '\n✅А также это может позволить Вам понять время, необходимое для работы '
                         f'и нашу низкую{emojize(":pinching_hand:")} ценовую политику.', reply_markup=MAIN_MENU)


@logger.catch
async def main_menu(message: types.Message):
    '''Обработчик для кнопки главного меню'''

    # отвечаем пользователю и отправляем ему клавиатуру
    await message.answer('Вы находитесь в ГЛАВНОМ МЕНЮ', reply_markup=MAIN_MENU)


@logger.catch
async def prepare_to_send_application(message: types.Message, state: FSMContext):
    '''Пользователь нажал на кнопку ЗАЯВКА и попал сюда, где мы предлагаем ему отправить заявку'''

    # убираем клавиатуру у пользователя
    await message.answer(f'Вы в разделе отправки заявки {emojize(":writing_hand:")}',
                         reply_markup=ReplyKeyboardRemove())
    await message.answer('⏩Вы можете кратко описать Вашу ситуацию, '
                         'с Вами свяжется мастер и обговорит детали.'
                         '\n⏩Также Вы можете указать свой номер телефона, если хотите, чтобы Вам перезвонили.'
                         '\n\n✅Напишите сообщение - оно и будет Вашей заявкой.'
                         f'\n\n{emojize(":information:")}Но важно понимать, что даже по фото или видео сложно оценить '
                         f'проблему... '
                         f'Для этого нужен взгляд живого человека, боты{emojize(":robot:")} тут, увы, бессильны...'
                         '\n\nНажмите сюда ❌ , чтобы не отправлять и вернуться в главное меню',
                         reply_markup=CANCEL_INLINE_KEYBOARD)

    # устанавливаем состояние пользователю "подготовка к отправке заявки"
    # не забываем указать state='*' в хэндлере для отмены отправки заявки,
    # иначе он будет работать только для объектов, у которых нет состояния,
    # а у нас, как мы наблюдаем, оно устанавливается.
    await ApplicationSendStates.prepare_to_send.set()


@logger.catch
async def cancel_send_application(call: CallbackQuery, state: FSMContext):
    '''Обработчик для нажатия кнопки отмены при отправке заявки'''
    # сбрасываем состояние
    await call.answer('Вы отменили отправку заявки для мастера', show_alert=True)
    await state.reset_state()
    await call.message.answer('Вы находитесь в ГЛАВНОМ МЕНЮ', reply_markup=MAIN_MENU)


@logger.catch
async def send_application(message: types.Message, state: FSMContext):
    '''Функция, в которой сообщение пользователя пересылается админам, как заявка'''
    user_id = message.from_user.id
    user_name = message.from_user.username
    text = message.text
    from_chat_id = message.chat.id
    message_id = message.message_id
    await BOT.forward_message(chat_id=ADMIN_ID, from_chat_id=from_chat_id, message_id=message_id)
    response = await post_create_new_application(tlg_user_id=user_id, tlg_user_name=user_name, application_text=text)
    # сбрасываем состояние пользователя
    await state.reset_state()
    await message.answer('Ваша заявка отправлена. Вы можете перейти на ГЛАВНОЕ МЕНЮ', reply_markup=CAT_LST_DTL_KEYBRD)


@logger.catch
async def send_contacts(message: types.Message):
    '''Обработчик для нажатия кнопки КОНТАКТЫ'''

    await message.answer(f'{emojize(":loudspeaker:")}Итак, наши контакты\n\n'
                         f'{emojize(":cityscape:")}Адрес: улица Пушкина 10\n'
                         f'{emojize(":telephone_receiver:")}Телефон: +7 777 777 77 78\n'
                         f'{emojize(":man_office_worker_light_skin_tone:")}Контактное лицо: Человек со знакомым именем.\n',
                         reply_markup=MAIN_MENU)


@logger.catch
async def some_video_sent_to_bot(message: types.Message):
    '''Обработчик для любых медиа-файлов и документов, присланных боту. Сообщения просто пересылаются админу.'''

    await BOT.send_message(
        chat_id=ADMIN_ID,
        text=f'Пользователь {message.from_user.username} c ID {message.from_user.id} прислал мне вот такие файлы.'
    )
    from_chat_id, message_id = message.chat.id, message.message_id
    await BOT.forward_message(chat_id=ADMIN_ID, from_chat_id=from_chat_id, message_id=message_id)


@logger.catch
def register_main_menu_handlers():
    '''Функция для регистрации обработчиков'''

    DP.register_message_handler(start_message, Command(['start', 'help']))
    DP.register_message_handler(main_menu, Text(equals=[KEYBOARD['HEAD_PAGE']]))
    DP.register_message_handler(prepare_to_send_application, Text(equals=KEYBOARD['APPLICATION']), state='*')
    DP.register_message_handler(send_application, state=ApplicationSendStates.prepare_to_send)
    DP.register_callback_query_handler(cancel_send_application, callback_for_cancel.filter(cancel='True'), state='*')
    DP.register_message_handler(send_contacts, Text(equals=[KEYBOARD['CONTACTS']]))
    DP.register_message_handler(
        some_video_sent_to_bot,
        content_types=types.ContentTypes.VIDEO | types.ContentTypes.PHOTO | types.ContentTypes.DOCUMENT | types.ContentTypes.AUDIO
    )
