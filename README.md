# Fuel Price Monitor Bot ⛽️🤖

Профессиональный Telegram‑бот для отслеживания цен на топливо на разных АЗС.  
Проект демонстрирует работу с SQLite, модульную архитектуру на Python и безопасное хранение конфиденциальных данных в `.env`.

---

## 🔍 Основные возможности

- **Отслеживание цен в реальном времени** — актуальные данные по стоимости топлива.
- **Логирование действий** — все запросы пользователей сохраняются в локальную базу данных.
- **Панель администратора** — аналитика (общее количество пользователей, кликов, топ‑5 популярных станций).
- **Безопасность** — токены и ключи хранятся в `.env`, чтобы избежать утечек.

---

## 🛠 Технологии

- **Язык**: Python 3.11+
- **Библиотека**: `pyTelegramBotAPI`
- **База данных**: SQLite3
- **Управление окружением**: `python-dotenv`

---

## 🚀 Установка

1. Клонировать репозиторий:

   ```bash
   git clone https://github.com/cyber-leak/fuel_price_monitor.git
   cd fuel_price_monitor
   ```

2. Создать виртуальное окружение и установить зависимости:

   ```bash
   python -m venv venv
   source venv/bin/activate  # на Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Создать `.env` файл с переменными:

   ```
   BOT_TOKEN=ваш_токен
   ADMIN_ID=692716613  # id администратора для команды /admin_stats
   ```

4. Запустить бота:
   ```bash
   python main.py
   ```

---

## 📁 Структура проекта

```
fuel_price_monitor/
├── main.py
├── database.py
├── handlers/
│   ├── __init__.py
│   └── fuel.py
├── keyboards/
│   ├── __init__.py
│   └── inline.py
├── test_parser.py
├── requirements.txt
└── .env
```

---

## 📝 Лицензия

MIT © [cyber-leak](https://github.com/cyber-leak)

---

Приятного использования!
