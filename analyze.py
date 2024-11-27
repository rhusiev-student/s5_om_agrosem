import pandas as pd


def get_same_nom_1(row: pd.Series, csv: pd.DataFrame) -> pd.DataFrame:
    nom_1 = row["Номенклатурна гр 1 рівень"]
    same_nom_2 = get_same_nom_2(row, csv)
    return same_nom_2[same_nom_2["Номенклатурна гр 1 рівень"] == nom_1]


def get_same_nom_2(row: pd.Series, csv: pd.DataFrame) -> pd.DataFrame:
    nom_2 = row["Номенклатурна гр 2 рівень"]
    return csv[csv["Номенклатурна гр 2 рівень"] == nom_2]


def get_similar_critical_code(
    row: pd.Series, csv: pd.DataFrame, radius: int
) -> pd.DataFrame:
    code = row["MEDIAN of Critical Code"]
    lower_bound = int(code) - radius
    upper_bound = int(code) + radius
    return csv[csv["MEDIAN of Critical Code"].between(lower_bound, upper_bound)]


def predict_month_using_similar(
    month_ago: int, row: pd.Series, similar: pd.DataFrame
) -> float:
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

for similar_code_radius, same_nom in [
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
]:
    print(f"{similar_code_radius=}, {same_nom=}")
    mse = 0
    i = 0
    for index, row in agrosem_csv.iterrows():
        if same_nom == 1:
            similar = get_same_nom_1(row, agrosem_csv)
        elif same_nom == 2:
            similar = get_same_nom_2(row, agrosem_csv)
        else:
            similar = agrosem_csv
        similar = get_similar_critical_code(row, similar, similar_code_radius)
        local_mse = 0
        for i in range(1, 13):
            actual_sales = float(row[f"Sales {i} months ago"])
            if not similar_code_radius and not same_nom:
                predicted_sales = predict_month_using_self(i, row)
            else:
                predicted_sales = predict_month_using_similar(i, row, similar)
            local_mse += (predicted_sales - actual_sales) ** 2
        mse += local_mse
        i += 1
    print("MSE:", mse / len(agrosem_csv) / 12)
