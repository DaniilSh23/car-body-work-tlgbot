import aiohttp
from loguru import logger
from settings.config import WORKS_CATEGORIES_API_URL, COMPLETED_WORKS_LST_API_URL, CREATE_NEW_APPLICATION_API_URL, \
    COMPLETED_WORK_DETAIL_API_URL


@logger.catch
async def get_works_categories():
    '''Запрос для получения списка всех категорий работ'''
    # создаём клиент сессии
    async with aiohttp.ClientSession() as session:
        # выполняем GET запрос по указанному в константе адресу
        async with session.get(WORKS_CATEGORIES_API_URL) as response:
            # ждём выполнения корутины ответа и формируем из ответа json
            return await response.json()


@logger.catch
async def get_works_list(category_id=None):
    '''Запрос для получения списка выполненных работ по данной категории.'''
    async with aiohttp.ClientSession() as session:
        if category_id:
            req_url = ''.join([COMPLETED_WORKS_LST_API_URL,'?id=', category_id])
        else:
            req_url = COMPLETED_WORKS_LST_API_URL
        async with session.get(req_url) as response:
            return await response.json()


@logger.catch
async def get_detail_info_about_work(work_id):
    '''Запрос для получения детальной информации о выполненной работе.'''
    async with aiohttp.ClientSession() as session:
        async with session.get(''.join([COMPLETED_WORK_DETAIL_API_URL, work_id])) as response:
            return await response.json()
            # data = await response.read()
            # return  json.loads(data)


@logger.catch
async def post_create_new_application(tlg_user_id, tlg_user_name, application_text):
    '''Запрос для создания новой заявки в БД'''
    async with aiohttp.ClientSession() as session:
        async with session.post(
                CREATE_NEW_APPLICATION_API_URL,
                headers={'Content-Type': 'application/json'},
                json={'tlg_user_id': tlg_user_id, 'tlg_user_name': tlg_user_name, 'application_text': application_text}
        ) as response:
            return await response.json()