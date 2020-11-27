import pandas as pd
from price import t, weighted_day_price
from core import tickers, dates
from os import path
from datetime import datetime
from iexfinance.stocks import get_historical_data, get_historical_intraday
from iexfinance.utils import exceptions as e

start = datetime(2020, 11, 24)
end = datetime(2020, 11, 25)
dt = datetime(2020, 11, 24)
dt_s = dt.strftime("%Y-%m-%d")

opdir = 'min_price'
processed_t = f'{opdir}/{dt_s}_processed.txt'
error_t = f'{opdir}/{dt_s}_error.txt'


def weighted_price_df(r):
    return weighted_day_price(r.open, r.close, r.high, r.low)


def to_csv(ticker, op, dt=dt, mode='min'):
    try:
        if mode == 'day':
            res = get_historical_data(ticker, start, end, token=t)
        elif mode =='min':
            res = get_historical_intraday(ticker, dt, token=t)
        else:
            print("Check your mode: {mode}, BYE")
            return
    except e.IEXQueryError as IQE:
        with open(error_t, 'a') as f:
            f.write(f"{ticker}\n")
        print(IQE.__context__)
        return

    df = pd.DataFrame(res).T

    df.insert(0, 'Ticker', ticker)

    df=df.reset_index().rename(columns={"index": 'Date'}).set_index(['Ticker', 'Date'])
    # df['weighted_avg'] = df.apply(weighted_price_df, 1).round(2)

    df.to_csv(op)


def to_csv_dedup(ticker, opdir=opdir, dt_s=dt_s):
    print(f"{ticker:<9}@{dt_s}:")
    op = f'{opdir}/{ticker}_{dt_s}_min.csv'
    if not path.exists(op):
        print(f"    start processing...")
        l = dt_s.split('-')
        Y, m, d = tuple(l)
        dt = datetime(int(Y), int(m), int(d))
        to_csv(ticker, op, dt)
    else:
        with open (processed_t, 'a') as f:
            f.write(f"{ticker}\n")
        print(f"    Skipped")


def get_csv_all_tickers(tickers=tickers, opdir=opdir):
    for ticker in tickers:
        to_csv_dedup(ticker, opdir)


def get_csv_all_tickers(tickers=tickers, dates=dates, opdir=opdir):
    for dt_s in dates:
        processed_t = f'{opdir}/{dt_s}_processed.txt'
        error_t = f'{opdir}/{dt_s}_error.txt'
        for ticker in tickers:
            to_csv_dedup(ticker, opdir, dt_s)


if __name__ == '__main__':
    get_csv_all_tickers()
