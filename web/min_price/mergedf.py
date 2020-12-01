import pandas as pd
from glob import glob

Ymm = '2020-10'
log = f'logs/mergedf_{Ymm}.txt'
op = f'ark_min_price_{Ymm}.csv'
files = f"data/*_{Ymm}-*_min.csv"

x = [f for f in glob(files)]

df = pd.DataFrame()

for i, f in enumerate(x):
    try:
        if i % 500 == 0:
            s = f"Processing {i:<5} : {f}\n"
            with open(fi, 'a') as fi:
                fi.write(s)
        _df = pd.read_csv(f)
    except pd.errors.EmptyDataError as pdeEDE:
        s = f"Empty data: {f}\n"
        with open(fi, 'a') as fi:
            fi.write(s)
    else:
        df = df.append(_df, ignore_index=True)


df.set_index(['Ticker']).to_csv(op)

# 82744
# 83423
# 83530
# 83649
# 83719
# 83743
# 83784
# 83818
# 83864
# 83898
