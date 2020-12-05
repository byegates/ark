import pandas as pd
from glob import glob

Ymm = '20201127_20201204'
mode = 'day'
files = f"data/*_2020-*_{mode}.csv"
log = f'log/merge_{mode}_{Ymm}.txt'
op = f'ark_{mode}_price_{Ymm}.csv'

x = [f for f in glob(files)]

df = pd.DataFrame()

for i, f in enumerate(x):
    try:
        if i % 500 == 0:
            s = f"Processing {i:<5} : {f}\n"
            with open(log, 'a') as fi:
                fi.write(s)
        _df = pd.read_csv(f)
    except pd.errors.EmptyDataError as pdeEDE:
        s = f"Empty data: {f}\n"
        with open(log, 'a') as fi:
            fi.write(s)
    else:
        df = df.append(_df, ignore_index=True)

df.set_index(['symbol']).to_csv(op)

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
