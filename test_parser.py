import requests
from bs4 import BeautifulSoup

url = "https://index.minfin.com.ua/markets/fuel/tm/"
response = requests.get(url)


while True:
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")

        if len(tables) > 0:
            target_brand = input("Введите название заправки (например, WOG или OKKO): ")

            rows = tables[0].find_all("tr")
            found = False

            # Пропускаем первую строку (шапку), так как ищем только по данным
            for row in rows[1:]:
                if target_brand.upper() in row.text.upper():

                    # Вытаскиваем все ячейки, сохраняя пустые места (чтобы ничего не сдвинулось)
                    cells = [cell.text.strip() for cell in row.find_all("td")]

                    # Защита: проверяем, что в строке действительно 7 или больше элементов
                    if len(cells) >= 7:
                        # Разбираем ячейки по их реальным позициям (индекс 1 пропускаем!)
                        name = cells[0]

                        # Конструкция 'val if val else "-"' значит:
                        # "возьми значение, но если там пустота '', то поставь прочерк"
                        p95_plus = cells[2] if cells[2] else "-"
                        a95 = cells[3] if cells[3] else "-"
                        a92 = cells[4] if cells[4] else "-"
                        diesel = cells[5] if cells[5] else "-"
                        gas = cells[6] if cells[6] else "-"

                        result = (
                            f"⛽️ Заправка: {name}\n"
                            f"🔹 А-95+: {p95_plus} грн\n"
                            f"🔹 А-95: {a95} грн\n"
                            f"🔹 А-92: {a92} грн\n"
                            f"🔹 Дизель: {diesel} грн\n"
                            f"🔸 Газ: {gas} грн"
                        )

                        print(result)
                        found = True
                        break

            if not found:
                print(f"❌ Заправка '{target_brand}' не найдена.")
        else:
            print("Таблицы не найдены.")
    else:
        print(f"Ошибка сети: {response.status_code}")
