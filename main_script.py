""" 
Це основний файл, який запускає інші файли на виконання і записує 
результати в папку results.
"""

import os
import subprocess
import sys


def install_dependencies():
    """Встановлення потрібних бібліотек із requirements.txt"""
    print("Встановлення бібліотек...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("Потрібні бібліотеки успішно встановлені.")
    except subprocess.CalledProcessError:
        print(
            "При встановлені бібліотек виникла помилка. Будь ласка, перевірте ваш `requirements.txt`."
        )


def run_script(script_name):
    """Виконує пайтон файли"""
    print(f"Виконується {script_name}...")
    try:
        subprocess.check_call([sys.executable, script_name])
        print(f"{script_name} успішно виконано.")
    except subprocess.CalledProcessError:
        print(
            f"При виконанні {script_name} виникла помилка. Перегляньте файл для виявлення помилок."
        )


def main():

    install_dependencies()

    run_script("preprocess.py")

    run_script("plot_each_months.py")

    run_script("split_by_pricepriority.py")

    run_script("analyze.py")
    print(
        "Результати обчислень потрібної кількості товарів для замовлення знаходяться у останній колонці all_purchase_plans.csv у папці results."
    )

    run_script("analyze_1_2.py")
    print(
        "Результати обчислень критичних коефіцієнтів знаходяться у останньому стовпці таблиці critical_coefficients у папці results."
    )

    run_script("analyze_1_3.py")
    print(
        "Результати обчислень критичності товару (False - не критичний, можна замовити раз в рік, True - критичний, потрібно замовляти частіше) знаходяться у останньому стовпці таблиці analysis_results_1_3 у папці results."
    )

    print("Всі завдання виконано.")
    print("  ")


if __name__ == "__main__":
    main()
