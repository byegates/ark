import pandas as pd
from glob import glob

x = [f for f in glob("data/*_min.csv")]

df = pd.DataFrame()

for f in x:
    try:
        _df = pd.read_csv(f)
    except pd.errors.EmptyDataError as pdeEDE:
        print(f"Empty data: {f}")
    else:
        df = df.append(_df, ignore_index=True)

df.set_index(['Ticker']).to_csv('ark_min_price_20201016_20201127.csv')
