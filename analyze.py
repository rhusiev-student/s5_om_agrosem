"""
Файл, в якому реалізовані різні алгоритми визначення кількості товару,
яку потрібно закупити для наявності на складі.
"""

import pandas as pd
import math


def get_same_nom_1(row: pd.Series, csv: pd.DataFrame) -> pd.DataFrame:
    """
    Ця функція спершу викликає `get_same_nom_2` для фільтрації DataFrame `csv`
    за номенклатурною групою 2-го рівня. Потім додатково звужує результат,
    залишаючи лише ті рядки, у яких номенклатурна група 1-го рівня також збігається
    зі значенням у переданому рядку `row`.

    Аргументи:
        row (pd.Series): Рядок, який містить значення для фільтрації.
        csv (pd.DataFrame): DataFrame, що містить товари з номенклатурними групами.

    Повертає:
        pd.DataFrame: Підтаблиця, яка включає тільки ті рядки, у яких значення
                      у колонках "Номенклатурна гр 1 рівень" і "Номенклатурна гр 2 рівень"
                      збігаються із `row`.
    """
    nom_1 = row["Номенклатурна гр 1 рівень"]
    same_nom_2 = get_same_nom_2(row, csv)
    return same_nom_2[same_nom_2["Номенклатурна гр 1 рівень"] == nom_1]


def get_same_nom_2(row: pd.Series, csv: pd.DataFrame) -> pd.DataFrame:
    """
    Порівнює рядки у яких значення у колонці "Номенклатурна гр 2 рівень"
    у таблиці csv
    співпадають із значеннями "Номенклатурна гр 2 рівень" у рядку row.

    Аргументи:
        row (pd.Series): Рядок, який містить значення для фільтрації.
        csv (pd.DataFrame): DataFrame, що містить товари з номенклатурними групами.

    Повертає:
        pd.DataFrame: Підтаблиця, яка включає тільки ті рядки, у яких значення
                      у колонці "Номенклатурна гр 2 рівень" збігається із `row`.
    """
    nom_2 = row["Номенклатурна гр 2 рівень"]
    return csv[csv["Номенклатурна гр 2 рівень"] == nom_2]


def get_similar_critical_code(
    row: pd.Series, csv: pd.DataFrame, radius: int
) -> pd.DataFrame:
    """
    Ця функція фільтрує переданий csv у яких значення в колонці
    "MEDIAN of Critical Code" знаходяться в межах переданого radius
    від заданого значення в рядку row.

    Аругменти:
        row (pd.Series): Рядок, який містить значення для фільтрації.
        csv (pd.DataFrame): DataFrame, що містить товари з номенклатурними групами.
        radius (int): Радіус діапазону "MEDIAN of Critical Code",
        що використовується для фільтрації

    Повертає:
        pd.DataFrame: DataFrame, який містить всі рядки з csv,
        у яких значення "MEDIAN of Critical Code" знаходяться в межах заданого радіусу.
    """
    code = row["MEDIAN of Critical Code"]
    lower_bound = int(code) - radius
    upper_bound = int(code) + radius
    return csv[csv["MEDIAN of Critical Code"].between(lower_bound, upper_bound)]


def predict_month_using_similar(
    month_ago: int, row: pd.Series, similar: pd.DataFrame
) -> float:
    """
    Функція виконує прогнозування продажів для вказаного місяця month_ago
    на основі записів із переданої таблиці даних similar для запису row.

    Аргументи:
        month_ago (int): Місяць, для якого робиться передбачення продажів
        row (pd.Series): Рядок, для якого робиться прогноз
        similar (pd.DataFrame): Таблиця даних, що містить записи посортовані за
            нуменклатурними групами 1 чи 1 та 2.

    Повертає:
        float: прогнозоване число продажів для місяці month_ago.
    """
    similar = similar[
        (similar[f"Sales {month_ago+12} months ago"] > 0)
        & (similar[f"Sales {month_ago+13} months ago"] > 0)
    ]
    if similar.empty:
        return predict_month_using_self(month_ago, row)
    similar_diff = (
        similar[f"Sales {month_ago+12} months ago"]
        / similar[f"Sales {month_ago+13} months ago"]
    )
    mean_diff = similar_diff.mean()
    return mean_diff * (row[f"Sales {month_ago+1} months ago"] + 0.01)


def predict_month_using_self(month_ago: int, row: pd.Series) -> float:
    """
    Функція, що обчислює число продажів для місяця month_ago
    на базі попередніх записів таблиці row.

    Аргументи:
        month_ago (int): Місяць, для якого робиться передбачення продажів
        row (pd.Series): Рядок, для якого робиться передбачення продажів.

    Повертає:
        float: прогнозоване число продажів для місяці month_ago.
    """
    year_ago = row[f"Sales {month_ago+12} months ago"]
    year_ago1 = row[f"Sales {month_ago+13} months ago"]
    if (
        f"Sales {month_ago+24} months ago" not in row
        or f"Sales {month_ago+25} months ago" not in row
    ):
        year2_ago = 0
        year2_ago1 = 0
    else:
        year2_ago = row[f"Sales {month_ago+24} months ago"]
        year2_ago1 = row[f"Sales {month_ago+25} months ago"]
    month_ago = row[f"Sales {month_ago+1} months ago"]
    if year_ago == 0 or year_ago1 == 0:
        if year2_ago == 0 or year2_ago1 == 0:
            return 0
        return year2_ago / year2_ago1 * month_ago
    return year_ago / year_ago1 * month_ago


agrosem_csv = pd.read_csv("data/agrosem_csv_highprice_highpriority.csv", sep=",")

lst_radius_nomenclature = [
    (0, 0),
    (0, 1),
    (0, 2),
    (5, 0),
    (5, 1),
    (5, 2),
    (10, 0),
    (10, 1),
    (10, 2),
    (15, 0),
    (15, 1),
    (15, 2),
    (20, 0),
    (20, 1),
    (20, 2),
    (25, 0),
    (25, 1),
    (25, 2),
]


def calculate_purchase_requirements(row: pd.Series, predicted_sales: float) -> float:
    """
    Розраховує кількість товарів, які потрібно дозамовити, щоб задовольнити прогнозовані продажі.

    Аргументи:
        row (pd.Series): Рядок з інформацією про товар.
        predicted_sales (float): Прогнозовані продажі на наступний місяць.

    Повертає:
        float: Кількість товару, яку потрібно дозамовити.
    """
    available_stock = row["SUM of Доступний залишок на складі"]
    reserved_stock = row["SUM of Зарезервовано на складі"]
    total_available = available_stock - reserved_stock
    purchase_quantity = max(0, predicted_sales - total_available)
    return purchase_quantity


all_purchase_plans = []

for similar_code_radius, same_nom in lst_radius_nomenclature:
    # print(" ")
    # print("Start-------------")
    # print(" ")
    # print(f"{similar_code_radius=}, {same_nom=}")
    mse = 0
    mae = 0
    count = 0

    for index, row in agrosem_csv.iterrows():
        if same_nom == 1:
            similar = get_same_nom_1(row, agrosem_csv)
        elif same_nom == 2:
            similar = get_same_nom_2(row, agrosem_csv)
        else:
            similar = agrosem_csv
        similar = get_similar_critical_code(row, similar, similar_code_radius)

        for i in range(1, 13):
            actual_sales = float(row[f"Sales {i} months ago"])
            if not similar_code_radius and not same_nom:
                predicted_sales = predict_month_using_self(i, row)
            else:
                predicted_sales = predict_month_using_similar(i, row, similar)
            mse += (predicted_sales - actual_sales) ** 2
            mae += abs(predicted_sales - actual_sales)
            count += 1

            purchase_quantity = calculate_purchase_requirements(row, predicted_sales)
            if purchase_quantity > 0:
                all_purchase_plans.append(
                    {
                        "Назва": row["Назва"],
                        "Номенклатурна гр 1 рівень": row["Номенклатурна гр 1 рівень"],
                        "Номенклатурна гр 2 рівень": row["Номенклатурна гр 2 рівень"],
                        "Місяць": f"Month {i}",
                        "Radius": similar_code_radius,
                        "Same Nom": same_nom,
                        "Потрібно закупити": math.ceil(purchase_quantity),
                    }
                )

    # print("MSE:", mse / count)
    # print("MAE:", mae / count)
    # print(" ")
    # print("End---------------")
    # print(" ")

if all_purchase_plans:
    combined_df = pd.DataFrame(all_purchase_plans)
    combined_df.to_csv(
        "./results/all_purchase_plans.csv", index=False, encoding="utf-8-sig"
    )
    print("Всі плани закупівель записано у файл: all_purchase_plans.csv в папці results")
