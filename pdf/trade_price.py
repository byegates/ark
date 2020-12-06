import tabula
import pandas as pd
import numpy as np

ip_dir = 'docs/'
op_dir = 'csv/'

files = {
    "ARK_Trades_asof_20200521.pdf",
    "ARK_Trades_asof_20201111.pdf",

    }

floats = ['price', 'low', 'high', 'close']
keys = ['date', 'action', 'symbol']
cols0 = keys + floats
cols1 = cols0 + ['last']
cols = keys + ['price']


invalid = {
    '#N/A N/A',
    '#########',
}


def fix_symbol(l):
    start_pos_price = 2 + (len(l) - 8) + 1
    return l[:2] + [' '.join(l[2:start_pos_price])] + l[start_pos_price:]


def to_float(s):
    return np.nan if s in invalid else s.replace('"', '').replace('$', '').replace(',', '')


def editdf0(df):
    df = df[8:]
    l = [[to_float(s) for s in df.iloc[i,0].split()] for i in range(len(df.index))]
    l = [ _ if len(_) == 8 else fix_symbol(_) for _ in l]
    df = pd.DataFrame(l, columns=cols1)
    return df[cols0]


def editdf(df):
    df = df[1:]
    df.columns = cols1
    return df[cols0]

def editdfn(l):
    df = pd.DataFrame()
    for _df in l:
        _df = editdf(_df)
        df = df.append(_df, ignore_index=True)
    _ = df[floats].applymap(lambda s: to_float(s)).astype(float)
    return pd.concat([df[keys], _], axis=1)


def edit_n_merge(l):
    df = pd.DataFrame()
    df0 = editdf0(l[0]) # first table is read differently than the rest
    dfn = editdfn(l[1:]) # rest of the table are read in same format
    df = df.append(df0, ignore_index=True).append(dfn, ignore_index=True)
    df['date'] = pd.to_datetime(df.date)
    return df.set_index(keys)

def read_pdf(f):
    l = tabula.read_pdf(f, pages='all')
    return edit_n_merge(l)

def main():
    for f in files:
        read_pdf(f"{ip_dir}{f}").to_csv(f"{op_dir}{f.split('.')[0]}.csv")


if __name__ == "__main__":
    main()