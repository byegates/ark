import pandas as pd
from price import t, weighted_day_price
from core import tickers
from os import path
from datetime import datetime
from iexfinance.stocks import get_historical_data
from iexfinance.utils import exceptions as e

start = datetime(2020, 11, 24)
end = datetime(2020, 11, 26)

opdir = 'day_price/20201126'
processed_t = f'{opdir}/processed.txt'
error_t = f'{opdir}/error.txt'


def weighted_price_df(r):
    return weighted_day_price(r.open, r.close, r.high, r.low)


def to_csv(ticker, op):
    try:
        res = get_historical_data(ticker, start, end, token=t)
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


def get_csv_all_tickers(tickers=tickers, opdir=opdir):
    for ticker in tickers:
        print(f"{ticker}:")
        op = f'{opdir}/{ticker}_2020_hist_price_ytd.csv'
        if not path.exists(op):
            print(f"    start processing...")
            to_csv(ticker, op)
        else:
            with open (processed_t, 'a') as f:
                f.write(f"{ticker}\n")
            print(f"    Skipped")
    return


if __name__ == '__main__':
    get_csv_all_tickers()
