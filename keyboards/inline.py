from telebot import types


def fuel_menu():
    # Создаем объект клавиатуры
    markup = types.InlineKeyboardMarkup()

    # Создаем кнопки. callback_data — это то, что бот "услышит", когда юзер нажмет кнопку
    btn_wog = types.InlineKeyboardButton(text="WOG", callback_data="fuel_wog")
    btn_okko = types.InlineKeyboardButton(text="OKKO", callback_data="fuel_okko")

    # Добавляем кнопки в ряд
    markup.add(btn_wog, btn_okko)

    return markup
