import telebot
import config 
from handlers.fuel import register_fuel_handlers
from keyboards import inline

# Создаем объект бота, используя токен из конфига
bot = telebot.TeleBot(config.TOKEN)


# "Регистрируем" обработчики, передавая им нашего бота
# fuel.register_fuel_handlers(bot)
inline.get_top_brands_keyboard()
register_fuel_handlers(bot)


if __name__ == "__main__":
    print("bot started....")
    bot.infinity_polling(none_stop=True)
