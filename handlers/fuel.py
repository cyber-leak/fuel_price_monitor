# handlers/fuel.py
import logging
import os

from telebot.types import CallbackQuery, Message

import database
import test_parser
from keyboards import inline

logger = logging.getLogger(__name__)


def register_fuel_handlers(bot):
    """Регистрирует обработчики сообщений и колбеков для бота.

    Все функции-обработчики определяются внутри чтобы иметь доступ к объекту
    `bot` и могут быть перенесены в отдельный модуль при необходимости.
    """

    @bot.message_handler(commands=["start"])
    def start(message: Message) -> None:
        """Приветственный экран, создание/обновление записи пользователя."""
        user_name = message.from_user.first_name
        # регистрируем пользователя в БД (безопасно - внутри функции есть try/except)
        database.add_user(message.from_user.id, user_name)

        welcome_text = (
            f"Привет, {user_name}! 👋\n\n"
            "Я помогу тебе узнать актуальную <b>стоимость топлива</b> на популярных АЗС Украины. ⛽️\n"
            "Данные берутся напрямую с сайта <b>Минфин</b>.\n\n"
            "<b>Что я умею:</b>\n"
            "✅ Показываю цены на <b>А-95+</b>, <b>А-95</b>, <b>А-92</b>, <b>Дизель</b> и <b>Газ</b>.\n"
            "✅ Работаю быстро и без лишней рекламы.\n\n"
            "Чтобы проверить цену, выбери заправку из меню ниже: 👇"
        )

        bot.send_message(
            message.chat.id,
            welcome_text,
            parse_mode="HTML",
            reply_markup=inline.get_top_brands_keyboard(),
        )

    # Хендлер для кнопок выбора бренда
    @bot.callback_query_handler(func=lambda call: call.data.startswith("brand_"))
    def callback_fuel(call: CallbackQuery) -> None:
        """Обрабатывает нажатие на кнопку с брендом и отправляет цену."""
        target_brand = call.data.replace("brand_", "")
        database.log_action(call.from_user.id, f"check_{target_brand}")

        try:
            answer = test_parser.get_fuel_price(target_brand)
        except Exception as exc:
            logger.exception("Ошибка при парсинге цены для %s: %s", target_brand, exc)
            answer = "😞 Не удалось получить данные. Попробуйте позже."

        bot.send_message(call.message.chat.id, answer, parse_mode="HTML")

    @bot.message_handler(commands=["admin_stats"])
    def admin_stats(message: Message) -> None:
        """Команда для администратора: выводит статистику по пользователям и запросам."""
        ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
        if message.from_user.id == ADMIN_ID:
            top_actions = database.get_top_actions()
            total_users, total_clicks = database.get_stats()
            stats_text = (
                f"📊 <b>СТАТИСТИКА БОТА</b>\n\n"
                f"👥 Всего пользователей: {total_users}\n"
                f"⛽️ Всего запросов цен: {total_clicks}\n\n"
                f"{top_actions}"
            )
            bot.send_message(message.chat.id, stats_text, parse_mode="HTML")
        else:
            # нечёткий ответ для посторонних
            bot.send_message(
                message.chat.id,
                "Я тебя не понимаю....🤔",
                parse_mode="HTML",
            )

    @bot.message_handler(func=lambda message: True)
    def handle_unknown_message(message: Message) -> None:
        """Отвечает на любые неизвестные текстовые сообщения подсказкой."""
        help_text = (
            "🤔 <b>Я пока не умею распознавать текст.</b>\n\n"
            "Чтобы получить актуальную информацию, пожалуйста, используйте кнопки меню. 👇\n\n"
            "ℹ️ Я анализирую <b>средние цены</b> по сетям АЗС, предоставленные финансовым порталом <b>Минфин</b>. "
            "Данные обновляются в режиме реального времени."
        )

        bot.send_message(
            message.chat.id,
            help_text,
            parse_mode="HTML",
            reply_markup=inline.get_top_brands_keyboard(),
        )
