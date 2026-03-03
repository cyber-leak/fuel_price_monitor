# handlers/fuel.py
from keyboards import inline


def register_fuel_handlers(bot):
    # Этот хендлер срабатывает на команду /fuel
    @bot.message_handler(commands=["fuel"])
    def start_fuel(message):
        bot.send_message(
            message.chat.id,
            "Выбери заправку для проверки цены.",
            reply_markup=inline.fuel_menu()
        )  # Прикрепляем нашу клавиатуру

    # А этот хендлер ловит нажатия на кнопки
    @bot.callback_query_handler(func=lambda call: call.data.startswith('fuel_'))
    def callback_fuel(call):
        if call.data == "fuel_wog":
            bot.edit_message_text("Цена на WOG: 55.00 грн", call.message.chat.id, call.message.message_id)
        elif call.data == "fuel_okko":
            bot.edit_message_text("Цена на OKKO: 54.79 грн", call.message.chat.id, call.message.message_id)
