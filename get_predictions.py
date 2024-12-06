import analyze
import os
import pandas as pd
import math

agrosem_csv = pd.read_csv("data/agrosem_csv_highprice_highpriority.csv", sep=",")

all_purchase_plans = []

radius = 0
radius_3 = 0

all_purchase_plans = []

for index, row in agrosem_csv.iterrows():
    similar_3 = analyze.get_same_nom_1(row, agrosem_csv)
    similar = agrosem_csv
    similar_3 = analyze.get_similar_critical_code(row, similar_3, radius_3)
    similar = analyze.get_similar_critical_code(row, similar, radius)

    predicted_sales = analyze.predict_month_using_self(0, row)
    predicted_sales_3 = analyze.predict_three_month_ahead_using_self(-2, row)
    std = analyze.get_std_for_month(-1, row)
    std_3 = analyze.get_std_for_month(-3, row)

    purchase_quantity = analyze.calculate_purchase_requirements(
        row, predicted_sales, std
    )
    purchase_quantity_3 = analyze.calculate_purchase_requirements(
        row, predicted_sales_3, std_3
    )
    all_purchase_plans.append(
        {
            "Назва": row["Назва"],
            "Номенклатурна гр 1 рівень": row[
                "Номенклатурна гр 1 рівень"
            ],
            "Номенклатурна гр 2 рівень": row[
                "Номенклатурна гр 2 рівень"
            ],
            "Потрібно закупити": math.ceil(purchase_quantity),
            "Потрібно закупити 3 місяці": math.ceil(purchase_quantity_3),
        }
    )

dir_name = "results"
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
file_path = os.path.join(dir_name, "predictions.csv")

with open(file_path, "w", newline="", encoding="utf-8") as file:
    if all_purchase_plans:
        combined_df = pd.DataFrame(all_purchase_plans)
        combined_df.to_csv(file, index=False)
