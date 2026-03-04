import os
import sqlite3

DB_NAME = "user.db"


def init_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
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
    conn.close()


def add_user(user_id, username):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)",
        (user_id, username),
    )
    conn.commit()
    conn.close()


def log_action(user_id, action):
    """ФУНКЦИЯ ЗАПИСИ: Сохраняем, что юзер нажал кнопку"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO activity_log (user_id, action) VALUES (?, ?)",
        (user_id, action),
    )
    conn.commit()
    conn.close()


def get_stats():
    """ФУНКЦИЯ ПОЛУЧЕНИЯ: Считаем цифры для админки"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM activity_log")
    total_clicks = cursor.fetchone()[0]  # Тут исправили fetchall на fetchone

    conn.close()
    return total_users, total_clicks
