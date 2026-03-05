import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_fuel_price(target_brand: str) -> str:
    """Получает цены на топливо для указанной сети.

    Парсит страницу Минфина с данными по АЗС. Возвращает строку, готовую для
    отправки пользователю. В случае ошибки сети или парсинга возвращает
    текст с объяснением.
    """
    url = "https://index.minfin.com.ua/markets/fuel/tm/"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as exc:
        logger.exception("Сетевая ошибка при запросе %s: %s", url, exc)
        return "Ошибка сети, попробуйте позже."

    # словарь синонимов
    synonyms = {
        "WOG": "WOG",
        "OKKO": "ОККО",
        "BVS": "BVS",
        "SOCAR": "SOCAR",
        "UKRNAFTA": "Укрнафта",
        "BRSM": "БРСМ-Нафта",
        "UPG": "UPG",
        "Motto": "Motto",
        "KLO": "KLO",
        "AMIC": "AMIC",
    }

    # обработка HTML
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")
    if not tables:
        logger.warning("На странице нет таблиц с ценами")
        return "Таблицы не найдены."

    if target_brand is None:
        raise ValueError("target_brand не должен быть None")

    search_query = synonyms.get(target_brand, target_brand)
    if search_query is None:
        raise ValueError("Поисковый запрос не может быть пустым (None)")

    rows = tables[0].find_all("tr")
    # Пропускаем первую строку (шапку)
    for row in rows[1:]:
        if search_query.lower() in row.text.lower():
            cells = [cell.text.strip() for cell in row.find_all("td")]
            if len(cells) >= 7:
                name = cells[0]
                p95_plus = cells[2] or "-"
                a95 = cells[3] or "-"
                a92 = cells[4] or "-"
                diesel = cells[5] or "-"
                gas = cells[6] or "-"
                return (
                    f"⛽️ Заправка: {name}\n"
                    f"🔹 А-95+: {p95_plus} грн\n"
                    f"🔹 А-95: {a95} грн\n"
                    f"🔹 А-92: {a92} грн\n"
                    f"🔹 Дизель: {diesel} грн\n"
                    f"🔸 Газ: {gas} грн"
                )
    return f"❌ Заправка '{target_brand}' не найдена."
