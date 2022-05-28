from aiogram.utils.callback_data import CallbackData


# задаём передаваемые в кнопку параметры
callback_for_inline = CallbackData('base_param', 'id', 'step')
callback_for_cancel = CallbackData('base_param', 'cancel')
