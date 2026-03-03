# handlers/fuel.py


def register_fuel_handlers(bot):
    @bot.message_handler(commands=["fuel"])
    def send_fuel_prices(message):
        user_name = message.from_user.first_name
        text = (
            f"Привет, {user_name}!\n\n"
            f"⛽️ Цены на топливо (WOG):\n"
            f"• А-95: 55.00 грн\n"
            f"• ДП: 52.00 грн"
        )

        bot.send_message(message.chat.id, text)
