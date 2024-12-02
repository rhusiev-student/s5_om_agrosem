"""
Цей файлик аналізує криичність товару із lowprice та highpriority
"""

import pandas as pd

df = pd.read_csv("./data/agrosem_csv_lowprice_lowpriority.csv", delimiter=",")

critical_threshold = 10

df["is_critical"] = (df["SUM of Доступний залишок на складі"] < critical_threshold) & (
    df["Sales this month"] > 0
)

critical_items = df[df["is_critical"]][
    [
        "Назва",
        "Номенклатурна гр 1 рівень",
        "Номенклатурна гр 2 рівень",
        "SUM of Доступний залишок на складі",
        "Sales this month",
    ]
]

months_columns = [
    col for col in df.columns if col.startswith("Sales ") and "months ago" in col
]

df["total_sales"] = df[months_columns].sum(axis=1)

output_df = df[
    [
        "Назва",
        "Номенклатурна гр 1 рівень",
        "Номенклатурна гр 2 рівень",
        "SUM of Доступний залишок на складі",
        "Sales this month",
        "total_sales",
        "is_critical",
    ]
]

output_df.to_csv("./results/analysis_results_1_3.csv", index=False)

print("Результати збережено у файл analysis_results_1_3.csv у папці results.")
