# handlers/fuel.py


def register_fuel_handlers(bot):
    @bot.message_handler(commands=['fuel'])
    def send_fuel_prices(message):
        user_name = message.from_user.first_name
        bot.send_message(message.chat.id, f"{user_name}, заправки WOG: 55 грн")