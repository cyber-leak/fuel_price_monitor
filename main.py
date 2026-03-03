import telebot
import config
from handlers import fuel
from keyboards import inline

# Создаем объект бота, используя токен из конфига
bot = telebot.TeleBot(config.TOKEN)


# "Регистрируем" обработчики, передавая им нашего бота
fuel.register_fuel_handlers(bot)
inline.fuel_menu()


if __name__ == "__main__":
    print("bot started....")
    bot.infinity_polling()
