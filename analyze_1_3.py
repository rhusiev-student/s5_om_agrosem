import pandas as pd

# Завантаження даних з CSV файлу
df = pd.read_csv('./data/agrosem_csv_lowprice_lowpriority.csv', delimiter=',')

# Визначаємо поріг для критичних залишків
critical_threshold = 10

# Створюємо нову колонку, яка позначатиме критичні товари
df['is_critical'] = (df['SUM of Доступний залишок на складі'] < critical_threshold) & (df['Sales this month'] > 0)

# Вибираємо критичні товари
critical_items = df[df['is_critical']][['Назва', 'Номенклатурна гр 1 рівень', 'Номенклатурна гр 2 рівень',
                                        'SUM of Доступний залишок на складі', 'Sales this month']]

# Обчислюємо сумарні продажі за останні кілька місяців
df['sales_last_3_months'] = df[['Sales 1 months ago', 'Sales 2 months ago', 'Sales 3 months ago']].sum(axis=1)

# Створення списку всіх місяців для аналізу
months_columns = [col for col in df.columns if col.startswith('Sales ') and 'months ago' in col]

# Розрахунок загальних продажів за всі місяці
df['total_sales'] = df[months_columns].sum(axis=1)

# Формування кінцевого датафрейму для запису
output_df = df[['Назва', 'Номенклатурна гр 1 рівень', 'Номенклатурна гр 2 рівень',
                'SUM of Доступний залишок на складі', 'Sales this month', 'sales_last_3_months', 
                'total_sales', 'is_critical']]

# Збереження результатів в CSV файл
output_df.to_csv('./data/analysis_results_1_3.csv', index=False)

print("Аналіз завершено! Результати збережено у файл ./data/analysis_results.csv")
