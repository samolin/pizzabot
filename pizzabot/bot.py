from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime
from aiogram.dispatcher.filters import Text

from config import TOKEN
from keyboards import *

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

time = '{:%d-%m-%Y %H:%M:%S}'.format(datetime.now())

class FSMAdmin(StatesGroup):
    size = State()
    pay = State()
    check = State()

async  def on_startup(_):
    print('Bot is online.', time)

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    keyboard_order = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard_order.add(*buttons_order)
    await message.reply('Бот поможет вам сделать заказ', reply_markup=keyboard_order)
    txt = message.from_user.first_name, str(message.from_user.id), time
    with open('log.txt', 'a') as log:
        for i in txt:
            log.write(i + '\t')
        log.write('\n')

@dp.message_handler(commands=['заказ'], state=None)
async def cm_start(message: types.Message):
    keyboard_size = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard_size.add(*buttons_size)
    await FSMAdmin.size.set()
    await message.reply('Выберите размер пиццы', reply_markup=keyboard_size)

@dp.message_handler(state=FSMAdmin.size)
async def size_of_the_pizza(message: types.Message, state: FSMContext):
    if message.text.lower() in buttons_size:
        keyboard_pay = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard_pay.add(*buttons_pay)
        async with state.proxy() as data:
            data['size'] = message.text
        await FSMAdmin.next()
        await message.answer('Как вы будите платить?', reply_markup=keyboard_pay)
    else:
        await message.answer('Пожалуйста, выберите размер')

@dp.message_handler(state=FSMAdmin.pay)
async def pay_method(message: types.Message, state: FSMContext):
    if message.text in buttons_pay:
        keyboard_confirm = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard_confirm.add(*buttons_confirm)
        async with state.proxy() as data:
            data['pay'] = message.text
        await FSMAdmin.next()
        await message.answer(f"Вы будите {data['size']} пиццу, оплата {data['pay']}? ", reply_markup=keyboard_confirm)
    else: await message.answer('Пожалуйста, выберите способ оплаты')


@dp.message_handler(state=FSMAdmin.check)
async def pay_method(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':
        message.text = 'true'
        async with state.proxy() as data:
            data['confirm'] = message
        await message.answer(f"Спасибо за заказ, уважаемый {message.from_user.first_name} всегда рады вам!")
        await state.finish()
    elif message.text.lower() == 'нет':
        await message.answer(f"До скорой встречи, {message.from_user.first_name}")
        await state.finish()
    else:
        await message.answer('Пожалуйста, подтвердите выбор')


@dp.message_handler()
async def hello(message: types.Message):
    keyboard_order = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard_order.add(*buttons_order)
    await message.answer('Привет! Я пока еще глупый бот, но тут ты можешь заказать пиццу, '\
                         'которая никогда не приедет', reply_markup=keyboard_order)

@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='отмена'), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)