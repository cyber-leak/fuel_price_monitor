from handlers import fuel
import telebot
import config 


# Создаем объект бота, используя токен из конфига
bot = telebot.Telebot(config.TOKEN)


# "Регистрируем" обработчики, передавая им нашего бота
fuel.register_fuel_handlers(bot)



if __name__ == '__main__':
    print("bot started....")   
    bot.infinity_polling()

