import os
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from emoji import emojize

# токен выдается при регистрации приложения
TOKEN = ''
# название БД
NAME_DB = 'auto-bot.sqlite'
# версия приложения
VERSION = '0.0.1'
# автор приложния
AUTHOR = 'User'
# Телеграм ID админов
ADMIN_ID = '1978587604'

# абсолютный путь до текущей директории этого файла
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

COUNT = 0

# кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOUWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLAY': '✅ Оформить заказ',
    'COPY': '©️',
    # новые кнопки
    'HEAD_PAGE': emojize(":house_with_garden: Главное меню"),
    'APPLICATION': emojize(':writing_hand:Заявка'),
    'CATEGORY': emojize(':racing_car:  Категории работ'),
    'CONTACTS': emojize(':mobile_phone: Контакты'),
    'WORK_LIST': emojize(':rescue_worker’s_helmet: Наши работы'),
    'CANCEL_SEND': emojize('❌'),
}

# id категорий продуктов
CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3,
}

# названия команд
COMMANDS = {
    'START': "start",
    'HELP': "help",
}

# URL адреса для запросов к АPI бота
DOMAIN_NAME = 'https://auto-bot-api.herokuapp.com'
WORKS_CATEGORIES_API_URL = f'{DOMAIN_NAME}/api/category/'
COMPLETED_WORKS_LST_API_URL = f'{DOMAIN_NAME}/api/completed_works_list/'
COMPLETED_WORK_DETAIL_API_URL = f'{DOMAIN_NAME}/api/completed_works_detail_description/'
CREATE_NEW_APPLICATION_API_URL = f'{DOMAIN_NAME}/api/applications/'

# объекты: бот, диспатчер, сторэдж для машины состояний
BOT = Bot(token=TOKEN, parse_mode='HTML')
STORAGE = MemoryStorage()
DP = Dispatcher(BOT, storage=STORAGE)