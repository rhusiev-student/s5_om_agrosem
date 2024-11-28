"""
Файл, який ділить товар на 4 категорії та записує їх у відповідіні файли:
високі продажі+критична наявність -> agrosem_csv_highprice_highpriority
високі продажі+некритична наявність -> agrosem_csv_highprice_lowpriority
невисокі продажі+критична наявність -> agrosem_csv_lowprice_highpriority
невисокі продажі+некритична наявність -> agrosem_csv_lowprice_lowpriority
"""
import pandas as pd

agrosem_csv = pd.read_csv("data/agrosem_dedup.csv", sep=",")

# leave only the ones that have median 'Sales of {i} + 12k months ago' > 15000
agrosem_csv["Median sales a moths"] = agrosem_csv[
    [f"Sales {i} + 12k months ago" for i in range(1, 13)]
].median(axis=1)

agrosem_csv_highprice = agrosem_csv[agrosem_csv["Median sales a moths"] > 300] # >15000?
agrosem_csv_lowprice = agrosem_csv[agrosem_csv["Median sales a moths"] <= 300] # <15000?

agrosem_csv_highprice_highpriority = agrosem_csv_highprice[
    agrosem_csv_highprice["MEDIAN of Critical Code"] <= 21
]
agrosem_csv_highprice_lowpriority = agrosem_csv_highprice[
    agrosem_csv_highprice["MEDIAN of Critical Code"] > 21
]
agrosem_csv_lowprice_highpriority = agrosem_csv_lowprice[
    agrosem_csv_lowprice["MEDIAN of Critical Code"] <= 21
]
agrosem_csv_lowprice_lowpriority = agrosem_csv_lowprice[
    agrosem_csv_lowprice["MEDIAN of Critical Code"] > 21
]

agrosem_csv_highprice_highpriority.to_csv(
    "data/agrosem_csv_highprice_highpriority.csv", sep=",", index=False
)
agrosem_csv_highprice_lowpriority.to_csv(
    "data/agrosem_csv_highprice_lowpriority.csv", sep=",", index=False
)
agrosem_csv_lowprice_highpriority.to_csv(
    "data/agrosem_csv_lowprice_highpriority.csv", sep=",", index=False
)
agrosem_csv_lowprice_lowpriority.to_csv(
    "data/agrosem_csv_lowprice_lowpriority.csv", sep=",", index=False
)
