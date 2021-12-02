from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from datetime import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import TOKEN

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class FSMAdmin(StatesGroup):
    size = State()
    pay = State()
    check = State()
    thanks = State()

async  def on_startup(_):
    print('Bot is online.', '{:%d-%m-%Y %H:%M:%S}'.format(datetime.now()))

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    await message.reply('Бот поможет вам сделать заказ')

@dp.message_handler(commands=['order'], state=None)
async def cm_start(message: types.Message):
    await FSMAdmin.size.set()
    await message.reply('Какую пиццу вы хотите? Большую или маленькую?')

@dp.message_handler(state=FSMAdmin.size)
async def size_of_the_pizza(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await FSMAdmin.next()
    await message.answer('Как вы будите платить?')


@dp.message_handler(state=FSMAdmin.pay)
async def pay_method(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pay'] = message.text
    await FSMAdmin.next()
    await message.answer(f"Вы будите {data['size']} пиццу, оплата {data['pay']}? ")
#    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
#    buttons = ['наличкой', 'по карте']
#    keyboard.add(*buttons)
#    await bot.send_message(message.from_user.id, 'Как вы будите платить?', reply_markup=keyboard)

@dp.message_handler(state=FSMAdmin.check)
async def pay_method(message: types.Message, state: FSMContext):
    if message.text == 'да':
        message.text = True
        async with state.proxy() as data:
            data['confirm'] = message.text
    await state.finish()
    await message.answer(data['confirm'])



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)