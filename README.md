# To run the analysis you need to:

1. first add the csv to `data/agrosem.csv` 
2. type in terminal `python main_script.py`



# Description of the working algorithm

The main purpose of all the scripts and csv files, using `main_script.py`

### 1: Installing all dependencies 

In this file requirements.txt we have all requirements that we need in this project

### 2: Preprocess.py 

In this file we rename columns and add new columns for more effective analysis. For this we use function `rename_sales_columns` [A function that renames and fills columns for each month for hits and sales] and Code that adds new columns to a table of data for further processing

### 3. Plot_each_months.py

A file that plots sales for each product in a table by month. We see plot during the run of the main_script.py

### 4. Analyze.py

In this file we analyze data with these functions: 

1) `get_same_nom_1` 
[This function first calls `get_same_nom_2` to filter the DataFrame `csv` according to the nomenclature group of the 2nd level. Then further narrows the result leaving only those rows in which the 1st level nomenclature group also matches with the value in the passed `row`.] 

2) `get_same_nom_2`
[Compares rows with values ​​in the "Nomenclature gr 2 level" column in the csv table coincide with the values ​of "Nomenclature gr 2 level" in row row.]

3) `get_similar_critical_code`
[This function filters the passed csv in which values ​​are in the column "MEDIAN of Critical Code" are within the given radius from the given value in row.]

4) `predict_month_using_similar`
[The function performs sales forecasting for the specified month month_ago based on the records from the passed data table similar for the row record.]

5) `predict_month_using_self`
[A function that calculates the number of sales for the month month_ago based on the previous records of the row table.]

6) `calculate_purchase_requirements`
[Calculates the number of items that must be reordered to meet projected sales.]

The results of calculating the required number of products for the order are in the last column of all_purchase_plans.csv in the results folder."

### 5. Analyze_1_2.py

A file that calculates critical availability ratios based on different discount sizes

We save our results in file `./results/critical_coefficients.csv`.

### 6. Analyze_1_3.py

This file analyzes the criticality of the product with lowprice and highpriority.

We save our results in file `./results/analysis_results_1_3.csv`.

Our results can be find in folder `results`.