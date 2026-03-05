![Python](https://img.shields.io/badge/Python-3.11-blue)
![Telegram](https://img.shields.io/badge/Telegram-Bot-blueviolet)
![SQLite](https://img.shields.io/badge/SQLite-ready-lightgrey)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

# Fuel Price Monitor Bot ⛽️🤖

**Коротко**: профессиональный Telegram‑бот для отслеживания цен на топливо в реальном времени по разным АЗС. Проект демонстрирует модульную архитектуру на Python, работу с SQLite и безопасное хранение секретов в `.env`.

**Портфолио‑готовый README** — кратко, структурированно и с инструкциями для локальной и контейнерной разработки.

**Overview**

- **Назначение**: собирать и показывать актуальные цены топлива, логировать пользовательские действия и предоставлять администратору статистику.
- **Архитектура**: модульная — обработчики в директории [handlers/](handlers/), клавиатуры в [keyboards/](keyboards/), логика работы с БД в [database.py](database.py).

**Features**

- **Реальное время**: актуальные данные по стоимости топлива.
- **Логирование**: все взаимодействия пользователей сохраняются в SQLite.
- **Панель администратора**: статистика — общее количество пользователей, количество кликов и топ‑5 станций.
- **Безопасность**: конфиденциальные данные через `.env`.

**Technologies**

- **Язык**: Python 3.11+
- **Telegram API**: pyTelegramBotAPI
- **База данных**: SQLite
- **Env**: python-dotenv
- **Контейнеризация**: Docker + docker-compose

**Installation**

1. Клонировать репозиторий:

```bash
git clone https://github.com/cyber-leak/fuel_price_monitor.git
cd fuel_price_monitor
```

2. Создать и активировать виртуальное окружение, установить зависимости:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Подготовить `.env` в корне проекта (пример):

```env
BOT_TOKEN=ваш_токен
ADMIN_ID=ваш_айди
```

4. Запуск локально:

```bash
python main.py
```

**Docker (опционально)**
В проект добавлены примеры `Dockerfile`, `docker-compose.yml` и файл `.env.example`.

1. Сборка и запуск через `docker-compose` (production/deploy):

```bash
docker-compose up -d --build
```

2. Пример `Dockerfile` (в корне проекта, уже добавлен):

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser
ENV PYTHONUNBUFFERED=1
CMD ["python", "main.py"]
```

3. Пример `docker-compose.yml` (в корне проекта, уже добавлен):

```yaml
version: '3.8'
services:
  bot:
    build: .
    env_file: .env
    restart: unless-stopped
    # volumes:
    #   - ./:/app  # включите для разработки без пересборки
```

4. Пример `.env` для контейнера: используйте `.env` или `.env.example` для копирования значений секретов.

Советы:

- Для webhook‑режима добавьте `ports` и настройте прокси/HTTPS.
- Для разработки можно монтировать код (`volumes`) и переопределять `CMD` в `docker-compose.override.yml`.

**Project Structure**

```
.
├── main.py            # Точка входа бота
├── database.py        # Работа с SQLite
├── handlers/          # Обработчики команд и колбэков
│   └── fuel.py
├── keyboards/         # Инлайн клавиатуры
│   └── inline.py
├── requirements.txt
├── README.md
└── .env.example       # Пример переменных окружения (по желанию)
```

**Usage**

- Добавьте `BOT_TOKEN` в `.env` и запустите `python main.py` или через Docker.
- Администратор может получить статистику с помощью команды `/admin_stats` (см. `ADMIN_ID`).

**Development**

- Код организован по модулям: расширять новые обработчики следует в каталоге [handlers/](handlers/).
- Клавиатуры и интерфейсные элементы — в [keyboards/](keyboards/).
- Для работы с БД используйте `database.py` и следуйте существующему API функций.

**License**

- MIT © cyber-leak

Если нужно, могу добавить пример `Dockerfile`, `docker-compose.yml` и `README`‑раздел с примерами Docker образа.
