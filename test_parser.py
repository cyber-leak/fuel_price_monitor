import requests  # Импортируем библиотеку (пакет)
from bs4 import BeautifulSoup

# 1. URL — это адрес сайта, куда мы пойдем.
# Давай для примера возьмем страницу Минфина с ценами на бензин.

url = "https://index.minfin.com.ua/markets/fuel/tm/"


# 2. Выполняем запрос.
# requests — это объект-библиотека.
# .get() — это МЕТОД этого объекта (действие "сходи и принеси").
# url — это АРГУМЕНТ (куда именно идти).
response = requests.get(url)

# 3. response — это ОБЪЕКТ-ОТВЕТ, который нам вернул сервер.
# У него есть СВОЙСТВО .status_code (числовой код ответа).

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table")

    if len(tables) > 0:
        # 1. Сначала спрашиваем название (в боте это будет нажатие кнопки)
        target_brand = input("Введите название заправки (например, WOG): ")

        found = False  # Флаг: нашли мы заправку или нет
        rows = tables[0].find_all("tr")

        for row in rows:
            # 2. Сравниваем ввод пользователя с текстом в строке
            # Добавим .upper(), чтобы "wog" и "WOG" были одинаковыми
            if target_brand.upper() in row.text.upper():
                cells = row.find_all("td")

                if len(cells) >= 6:
                    name = cells[0].text.strip()
                    p95 = cells[1].text.strip()
                    a95 = cells[2].text.strip()
                    diesel = cells[4].text.strip()
                    gas = cells[5].text.strip()

                    result = (
                        f"⛽️ Заправка: {name}\n"
                        f"🔹 А-95+: {p95} грн\n"
                        f"🔹 А-95: {a95} грн\n"
                        f"🔹 Дизель: {diesel} грн\n"
                        f"🔸 Газ: {gas} грн"
                    )
                    print(result)
                    # Выводим результат
                    found = True
                    break  # Останавливаем цикл, так как заправка найдена

        if not found:
            print(f"❌ Заправка '{target_brand}' не найдена в списке.")
