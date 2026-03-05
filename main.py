import logging
import os

import telebot
from dotenv import load_dotenv

import database
from handlers.fuel import register_fuel_handlers
from keyboards import inline

# загрузка переменных окружения из .env
load_dotenv()

# минимальная настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен бота должен храниться в .env (BOT_TOKEN) для безопасности
token = os.getenv("BOT_TOKEN")
if not token:
    raise ValueError("BOT_TOKEN environment variable is required")

# создаём объект бота
bot = telebot.TeleBot(token)

# Инициализация базы данных до регистрации обработчиков
database.init_db()

# Регистрируем хендлеры
register_fuel_handlers(bot)

# вызываем вспомогательную функцию, чтобы проверить, что клавиатура строится
inline.get_top_brands_keyboard()


if __name__ == "__main__":
    print("bot started....")
    bot.infinity_polling(none_stop=True)


# Final production-ready refactor
