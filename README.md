first add the csv to `data/agrosem.csv` and install dependencies (`pip install -r requirements.txt`, possibly in venv)

then run `preprocess.py`

to plot the distribution by month for each item, run `plot_each_months.py`

to split the data into high and low critical code and high and low price, run `split_by_pricepriority.py`

run `analyze.py` to analyze, which method to use to predict next month's buyers. feel free to add other methods to predict
