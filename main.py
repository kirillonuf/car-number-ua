import logging
import requests

from aiogram import Bot, Dispatcher, executor, types

from config import API_TOKEN, KEY

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
                        f"Hi,{message.from_user.full_name}!\n"
                        f"It's my first BOT.I want to give information by car number")


@dp.message_handler()
async def echo(message: types.Message):
    number = message.text.upper()
    url = f"https://baza-gai.com.ua/nomer/{number}"
    r = requests.get(url, headers={"Accept": "application/json", "X-Api-Key": KEY})
    data = r.json()

    if 'error' in data:
        return await message.answer("Такого номера не знайдено")

    if data['is_stolen']:
        is_stolen = f"Так {data['stolen_details']}"
    else:
        is_stolen = "Ні"

    operations = ''
    for item in data['operations']:
        if item['is_registered_to_company']:
            is_company = "Так"
        else:
            is_company = "Ні"
        operations += (f"Тип: <b>{item['kind']['ua']}</b>\n"
                       f"Колір: <b>{item['color']['ua']}</b>\n"
                       f"Рік випуску: <b>{item['model_year']}</b>\n"
                       f"Дата реєстрації: <b>{item['registered_at']}</b>\n"
                       f"Реєстрація на компанію: <b>{is_company}</b>\n"
                       f"Операція: <b>{item['operation_group']['ua']}</b>\n"
                       f"Деталі операції: <b>{item['operation']['ua']}</b>\n"
                       f"Адреса: <b>{item['address']}</b>\n")

    await message.answer(f"Номер: <b>{data['digits']}</b>\n"
                         f"Марка: <b>{data['vendor']}</b>\n"
                         f"Модель: <b>{data['model']}</b>\n"
                         f"{operations}"
                         f"\n\nВикрадено: <b>{is_stolen}</b>\n\n"

                         f"Фото:\n<b>{data['photo_url']}</b>\n"
                         , parse_mode='html')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
