from price import t, weighted_day_price
import pandas as pd
from core import tickers, dates
from os import path
from datetime import datetime
from iexfinance.stocks import get_historical_data, get_historical_intraday
from iexfinance.utils import exceptions as e

logdir = 'min_price/logs/by_date'
datadir = 'min_price/data'
tickers_to_skip = set(
    [
        '3402',
        '3690',
        '4689',
        '6060',
        '8473',
        'ADYEN',
        'ALMDG',
        'AM3D',
        'ARCT UQ',
        'BATM',
        'BEZQ',
        'DANE',
        'DSY',
        'FTAL',
        'HEN3',
        'HEXAB',
        'MDT UN',
        'MOG/A',
        'OERL',
        'ONVO',
        'ONVO ',
        'STMN',
        'TAK UN',
        'TREE UW',
        'URGN UQ',
        'XRX UN',
        ]
    )


def weighted_price_df(r):
    return weighted_day_price(r.open, r.close, r.high, r.low)


def to_csv(ticker, op, dt, process_log, err_log, mode='min'):
    try:
        if mode == 'day':
            res = get_historical_data(ticker, start, end, token=t)
        elif mode == 'min':
            res = get_historical_intraday(ticker, dt, token=t)
        else:
            print("Check your mode: {mode}, BYE")
            return
    except e.IEXQueryError as IQE:
        with open(err_log, 'a') as f:
            _ = f"'{ticker}'"
            f.write(f"{_:<12} {'IEXQueryError'}\n")
        return

    if mode == 'day':
        df = pd.DataFrame(res).T
    elif mode == 'min':
        df = pd.DataFrame(res)

    df.insert(0, 'Ticker', ticker)

    if mode == 'day':
        df=df.reset_index().rename(columns={"index": 'Date'}).set_index(['Ticker', 'Date'])
    elif mode == 'min':
        df=df.set_index(['Ticker'])
    # df['weighted_avg'] = df.apply(weighted_price_df, 1).round(2)

    df.to_csv(op)
    with open (process_log, 'a') as f:
        f.write(f"{op:<45}: File written\n")


def to_csv_dedup(ticker, dt_s, datadir, process_log, err_log):
    op = f'{datadir}/{ticker}_{dt_s}_min.csv'
    if ticker in tickers_to_skip:
        with open (err_log, 'a') as f:
            f.write(f"{op:<45}: skipped for known IEXQueryError\n")
        return
    if not path.exists(op):
        dt = datetime.strptime(dt_s, '%Y-%m-%d')
        to_csv(ticker, op, dt, process_log, err_log)
    else:
        with open (process_log, 'a') as f:
            f.write(f"{op:<45}: File exist, skipped\n")


def get_csv_all_tickers(tickers=tickers, datadir=datadir):
    for ticker in tickers:
        to_csv_dedup(ticker, datadir)


def get_csv_all_dates(dates=dates, tickers=tickers, datadir=datadir):
    for dt_s in dates:
        process_log = f'{logdir}/{dt_s}_processed.txt'
        err_log = f'{logdir}/{dt_s}_error.txt'
        for ticker in tickers:
            to_csv_dedup(ticker, dt_s, datadir, process_log, err_log)


def main():
    from min_price import get_trade_days
    dts = get_trade_days.main()[174:]
    get_csv_all_dates(dates=dts)


if __name__ == '__main__':
    get_csv_all_tickers()
