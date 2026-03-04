# handlers/fuel.py
import test_parser
from keyboards import inline


def register_fuel_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        user_name = message.from_user.first_name

        text = (
            f"Привет, {user_name}! 👋\n\n"
            "Я помогу тебе узнать актуальную **стоимость топлива** на популярных АЗС Украины. ⛽️\n"
            "Данные берутся напрямую с сайта **Минфин**.\n\n"
            "**Что я умею:**\n"
            "✅ Показываю цены на **А-95+**, **А-95**, **А-92**, **Дизель** и **Газ**.\n"
            "✅ Работаю быстро и без лишней рекламы.\n\n"
            "Чтобы проверить цену, выбери заправку из меню ниже: 👇"
        )

        bot.send_message(
            message.chat.id,
            text,
            parse_mode="Markdown",
            reply_markup=inline.get_top_brands_keyboard(),
        )

    # А этот хендлер ловит нажатия на кнопки
    @bot.callback_query_handler(func=lambda call: call.data.startswith("brand_"))
    def callback_fuel(call):
        target_brand = call.data.replace("brand_", "")

        answer = test_parser.get_fuel_price(target_brand)
        bot.send_message(call.message.chat.id, answer)

    @bot.message_handler(func=lambda message: True)
    def handle_unknow_message(message):
        help_text = (
            "🤔 **Я пока не умею распознавать текст.**\n\n"
            "Чтобы получить актуальную информацию, пожалуйста, используйте кнопки меню. 👇\n\n"
            "ℹ️ Я анализирую **средние цены** по сетям АЗС, предоставленные финансовым порталом **Минфин**. Данные обновляются в режиме реального времени."
        )

        bot.send_message(
            message.chat.id,
            help_text,
            parse_mode="Markdown",
            reply_markup=inline.get_top_brands_keyboard(),
        )
