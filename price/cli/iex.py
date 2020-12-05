import pandas as pd
from os import path
from datetime import datetime
import pytz
from iexfinance.stocks import get_historical_data, get_historical_intraday
from iexfinance.utils import exceptions as e
from cli.config import symbols_to_skip, dates, symbols 

logdir = 'log'
datadir = 'data'

def dt10to8(s):
    return ''.join(s.split('-'))


def dt8to10(s):
    return f"{s[:4]}-{s[4:6]}-{s[6:]}"


def get_token(fi='dont.mess.with.me'):
    with open(fi, 'r') as f:
        return f.readline().strip()

t = get_token()

def dt_f(dt_s, fmt='%Y-%m-%d'):
    return datetime.strptime(dt_s, fmt)


def to_csv(ticker, op, dt, err_log, mode):
    try:
        if mode == 'day':
            res = get_historical_data(ticker, dt, token=t)
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

    df.insert(0, 'symbol', ticker)

    if mode == 'day':
        df=df.reset_index().rename(columns={"index": 'Date'}).set_index(['symbol', 'Date'])
    elif mode == 'min':
        df=df.set_index(['symbol'])

    df.to_csv(op)


def to_csv_dedup(ticker, dt_s, datadir, err_log, mode):
    op = f'{datadir}/{ticker}_{dt_s}_{mode}.csv'
    if ticker in symbols_to_skip:
        with open (err_log, 'a') as f:
            f.write(f"{op:<45}: skipped for known IEXQueryError\n")
        return
    if not path.exists(op):
        dt = dt_f(dt_s)
        to_csv(ticker, op, dt, err_log, mode)


def get_csv_all_symbols(symbols=symbols, datadir=datadir, mode='day'):
    for ticker in symbols:
        to_csv_dedup(ticker, datadir, err_log, mode)


def get_csv_all_dates(dates=dates, symbols=symbols, datadir=datadir, mode='day'):
    for dt_s in dates:
        err_log = f'{logdir}/{dt_s}_{mode}_error.txt'
        for ticker in symbols:
            to_csv_dedup(ticker, dt_s, datadir, err_log, mode)


def main():
    dts = dates[:6]
    get_csv_all_dates(dates=dts, mode='day')


if __name__ == '__main__':
    get_csv_all_symbols()
