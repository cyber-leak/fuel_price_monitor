from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_top_brands_keyboard() -> InlineKeyboardMarkup:
    """Строит клавиатуру с кнопками для выбора топ-АЗС.

    Возвращает объект `InlineKeyboardMarkup`, используемый в сообщениях.
    """
    markup = InlineKeyboardMarkup()

    # Создаем кнопки и задаём callback_data, по которому поймёт бот
    buttons = [
        InlineKeyboardButton(text="WOG", callback_data="brand_WOG"),
        InlineKeyboardButton(text="OKKO", callback_data="brand_OKKO"),
        InlineKeyboardButton(text="BVS", callback_data="brand_BVS"),
        InlineKeyboardButton(text="Socar", callback_data="brand_SOCAR"),
        InlineKeyboardButton(text="UKRNAFTA", callback_data="brand_UKRNAFTA"),
        InlineKeyboardButton(text="БРСМ-Нафта", callback_data="brand_BRSM"),
        InlineKeyboardButton(text="UPG", callback_data="brand_UPG"),
        InlineKeyboardButton(text="Motto", callback_data="brand_Motto"),
        InlineKeyboardButton(text="KLO", callback_data="brand_KLO"),
        InlineKeyboardButton(text="AMIC", callback_data="brand_AMIC"),
    ]

    for i in range(0, len(buttons), 2):
        markup.row(buttons[i], buttons[i + 1])

    return markup
