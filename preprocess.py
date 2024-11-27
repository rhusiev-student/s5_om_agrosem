import pandas as pd
import re

agrosem_csv = pd.read_csv("data/agrosem.csv", sep=",")

agrosem_csv["Назва"] = agrosem_csv["Назва"].str.strip()
agrosem_csv["Номенклатурна гр 1 рівень"] = agrosem_csv[
    "Номенклатурна гр 1 рівень"
].str.strip()
agrosem_csv["Номенклатурна гр 2 рівень"] = agrosem_csv[
    "Номенклатурна гр 2 рівень"
].str.strip()

agrosem_csv = agrosem_csv.groupby(
    [
        "Назва",
        "Номенклатурна гр 1 рівень",
        "Номенклатурна гр 2 рівень",
        "К-сть в упаковці",
        "Кратність продаж",
    ],
    as_index=False,
).agg(
    {
        "MEDIAN of Critical Code": "median",
        "MAX of Прайс": "max",
    }
    | {col: "sum" for col in agrosem_csv.columns if col.startswith("SUM")}
)


def rename_sales_columns(df):
    df_renamed = df.copy()

    for col in df_renamed.columns:
        if col.startswith("SUM of Продажі"):
            match = re.search(r"(\d+)", col)
            if match:
                number = match.group(1)
                new_name = f"Sales {number} months ago"
                df_renamed = df_renamed.rename(columns={col: new_name})
        if col.startswith("SUM of Хіти"):
            match = re.search(r"(\d+)", col)
            if match:
                number = match.group(1)
                new_name = f"Hits {number} months ago"
                df_renamed = df_renamed.rename(columns={col: new_name})

    df_renamed = df_renamed.rename(
        columns={"SUM of Продажі з початку місяця": "Sales this month"}
    )
    df_renamed = df_renamed.rename(
        columns={"SUM of Хіти поточного місяця": "Hits this month"}
    )
    return df_renamed


agrosem_csv = rename_sales_columns(agrosem_csv)

for i in range(1, 13):
    agrosem_csv[f"Sales {i} + 12k months ago"] = agrosem_csv[f"Sales {i} months ago"]
    j = 0
    while True:
        if f"Sales {i + 12 * j} months ago" in agrosem_csv.columns:
            agrosem_csv[f"Sales {i} + 12k months ago"] += agrosem_csv[
                f"Sales {i + 12 * j} months ago"
            ]
            j += 1
            continue
        agrosem_csv[f"Sales {i} + 12k months ago"] *= agrosem_csv["MAX of Прайс"]
        break

agrosem_csv.to_csv("data/agrosem_dedup.csv", sep=",", index=False)
