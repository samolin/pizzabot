from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
TOKEN='2120052018:AAGDnGcyWCxt46ZvRdY5vTRP7t4aUyL3lxU'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(msg: types.Message):
    await msg.reply_to_message(f'Салам аллейкум дорогой {msg.from_user.first_name}')

@dp.message_handler(content_types=['text'])
async def get_text_messages(msg: types.Message):
    if msg.text.lower() == 'привет':
        await msg.answer('Салам, брат!')
    else:
        await msg.answer('Лее брат не понимаю')

if __name__ == '__main__':
    executor.start_polling(dp)
