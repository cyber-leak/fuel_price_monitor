import logging
import sqlite3
from typing import Tuple

# -----------------------------------------

DB_NAME = "user.db"
# Простейшая настройка логирования на модульном уровне
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db() -> None:
    """Инициализирует базу данных: создаёт файлы и таблицы, если их нет.

    Безопасно вызывается при каждом старте бота. В случае ошибки она просто
    логируется и не прерывает работу приложения.
    """
    try:
        with sqlite3.connect(DB_NAME, check_same_thread=False) as conn:
            cursor = conn.cursor()
            # Таблица юзеров
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            # Таблица кликов
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.exception("Ошибка при инициализации базы данных: %s", e)


def add_user(user_id: int, username: str) -> None:
    """Добавляет пользователя в таблицу `users`.

    Если пользователь уже есть, то запрос игнорируется благодаря
    `INSERT OR IGNORE`.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
                (user_id, username),
            )
            conn.commit()
    except sqlite3.Error as e:
        logger.exception("Не удалось добавить пользователя %s: %s", user_id, e)


def log_action(user_id: int, action: str) -> None:
    """Сохраняет действие пользователя в лог.

    При любых ошибках записывает исключение в лог, но не поднимает его дальше.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO activity_log (user_id, action) VALUES (?, ?)",
                (user_id, action),
            )
            conn.commit()
    except sqlite3.Error as e:
        logger.exception(
            "Ошибка записи действия %s для пользователя %s: %s", action, user_id, e
        )


def get_stats() -> Tuple[int, int]:
    """Возвращает общее количество пользователей и кликов.

    Возвращает пару `(total_users, total_clicks)`. В случае ошибки возвращает
    `(0, 0)` и логирует проблему.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM activity_log")
            total_clicks = cursor.fetchone()[0]
            return total_users, total_clicks
    except sqlite3.Error as e:
        logger.exception("Не удалось получить статистику: %s", e)
        return 0, 0


def get_top_actions() -> str:
    """Собирает и форматирует строку для админской команды.

    Возвращает HTML-текст с пятью самыми частыми действиями. Действия
    очищаются от префикса `check_` и выводятся с эмодзи 📍. Если данных нет,
    возвращается человекочитаемое сообщение.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            query = (
                "SELECT action, COUNT(*) FROM activity_log "
                "GROUP BY action ORDER BY COUNT(*) DESC LIMIT 5"
            )
            cursor.execute(query)
            results = cursor.fetchall()
    except sqlite3.Error as e:
        logger.exception("Ошибка при получении топ‑действий: %s", e)
        return "<b>ТОП-5 ЗАПРОСОВ:</b> данных нет из-за ошибки."

    if not results:
        return "📊 Данных о кликах пока нет. Стань первым! 😉"

    top_text = "<b>ТОП-5 ЗАПРОСОВ:</b>\n"
    for action, count in results:
        brand_name = action.replace("check_", "")
        top_text += f"📍 {brand_name}: {count} кликов\n"

    return top_text
