from datetime import datetime
from cli.token import t as token_p
import json
import requests
import pytz
import pandas as pd
from cli.config import u, t, symbols_to_skip, symbols, dates, day_price_cols, errors, client, est_now


def get_url(tk='TSLA', dt='20201202', ty='day', env='test'):
    if ty == 'day':
        return f"{u[env]}{tk}/chart/date/{dt}?chartByDay=true&token={t[env]}"
    elif ty in stand_ty:
        return f"{u[env]}{tk}/{ty}/?token={t[env]}"


def get(tk='TSLA', dt='20201202', ty='day', env='test'):
    url = get_url(tk, dt, ty, env)
    res = requests.get(url)
    if res.content in errors: 
        print(f"url: {url}")
        print(f"status_code: {res.status_code}, content: {res.content}")
        return pd.DataFrame()
    else:
        return res2df(res.json(), tk, ty)


def res_edit(res, ty):
    if ty == 'ohlc':
        res['open'] = res['open']['price']
        res['close'] = res['close']['price']
        res['date'] = est_now().strftime("%Y-%m-%d")
        return [res]
    elif ty == 'quote':
        return [res]
    else:
        return res


def min2day(df):
    recs = [
        {
            'symbol': df['symbol'][0],
            'date': df['date'][0],
            'open': df['marketOpen'][0],
            'high': df['high'].max(),
            'low': df['low'].min(),
            'close': df['marketClose'][len(df.index)-1],
            'volume': df['volume'].sum(),
        }
    ]
    return pd.DataFrame(recs)


def res2df(res, tk='TSLA', ty='day'):
    df = pd.DataFrame((res_edit(res, ty)))
    if ty in {'day', 'ohlc'}:
        df = df[day_price_cols]#.set_index('symbol')
    elif ty == 'intraday-prices':
        df.insert(0, 'symbol', tk)
    
    return df


def main():
    return


if __name__ == '__main__':
    main()
