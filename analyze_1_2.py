"""
Файл, який обчислює критичні коефіцієнти наявності на основі різних розмірів знижок
"""
import pandas as pd
import numpy as np

filename = "data/agrosem_csv_highprice_lowpriority.csv"
data = pd.read_csv(filename)
discounts = np.arange(0, 0.55, 0.05)
results = {"Discount (%)": [], "Назва": [], "CriticalCoefficient": []}

for discount in discounts:
    for _, row in data.iterrows():
        if row["SUM of Доступний залишок на складі"] > 0:
            critical_coefficient = (row["MAX of Прайс"] * (1 - discount)) / row[
                "MAX of Прайс"
            ]
        else:
            critical_coefficient = float("inf")

        if critical_coefficient == float("inf") or pd.isna(critical_coefficient):
            result_value = "Критичний коефіцієнт неможливо обчислити, inf"
        else:
            result_value = critical_coefficient

        results["Discount (%)"].append(discount * 100)
        results["Назва"].append(row["Назва"])
        results["CriticalCoefficient"].append(result_value)

results_df = pd.DataFrame(results)

output_filename = "./results/critical_coefficients.csv"
results_df.to_csv(output_filename, index=False)
print(f"Результати збережено у файл: {output_filename} у папці results.")
