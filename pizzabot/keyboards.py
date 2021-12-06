from aiogram import types

#keyboard_order = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons_order = ['/заказ']

#keyboard_size = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons_size = ['маленькую', 'среднюю', 'большую']

keyboard_pay = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons_pay = ['наличкой', 'картой']

keyboard_confirm = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
buttons_confirm = ['да', 'нет']