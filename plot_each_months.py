"""
Файл, який будує графік продажів для кожного товару в таблиці по місяцях
"""

import pandas as pd
import matplotlib.pyplot as plt

agrosem_csv = pd.read_csv("data/agrosem_dedup.csv", sep=",")

plt.figure(figsize=(10, 8))

for index, row in agrosem_csv.iterrows():
    plt.plot(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        [
            row["Sales 1 + 12k months ago"],
            row["Sales 2 + 12k months ago"],
            row["Sales 3 + 12k months ago"],
            row["Sales 4 + 12k months ago"],
            row["Sales 5 + 12k months ago"],
            row["Sales 6 + 12k months ago"],
            row["Sales 7 + 12k months ago"],
            row["Sales 8 + 12k months ago"],
            row["Sales 9 + 12k months ago"],
            row["Sales 10 + 12k months ago"],
            row["Sales 11 + 12k months ago"],
            row["Sales 12 + 12k months ago"],
        ],
    )
plt.xlabel("Місяці року")
plt.ylabel("Кількість продажів")
plt.title("Динаміка продажів за місяцями (натисніть на хрестик, щоб продовжити роботу).")
plt.xticks(range(1, 13), ["Січ", "Лют", "Бер", "Кві", "Тра", "Чер", "Лип", "Сер", "Вер", "Жов", "Лис", "Гру"])
plt.grid(True)

plt.tight_layout()
plt.show()