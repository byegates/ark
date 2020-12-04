from datetime import datetime
from cli.token import t as token_p
import yaml, json
import requests
import pytz


with open('api.yaml') as f:
    api = yaml.load(f, Loader=yaml.FullLoader)

stand_ty = { # standard request types
    'quote', # 1
    'ohlc', # 1
    'intraday-prices', # 50 msgs
    'price-target', # require accesses?
}


u, t = api['iex']['u'], api['iex']['t']

day_price_cols = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']


cur_dt = datetime.today().strftime('%Y-%m-%d')


def get_url(tk='TSLA', dt='20201202', ty='day', env='test'):
    if ty == 'day':
        return f"{u[env]}{tk}/chart/date/{dt}?chartByDay=true&token={t[env]}"
    elif ty in stand_ty: # quote: 1 msg ohlc: 1
        return f"{u[env]}{tk}/{ty}/?token={t[env]}"


def get(tk='TSLA', dt='20201202', ty='day', env='test'):
    url = get_url(tk, dt, ty, env)
    res = requests.get(url)
    if res == b'Unknown symbol': 
        # Wrong date: b'You have supplied invalid values for this request'
        # U: same
        return pd.DataFrame()
    else:
        return res2df(res.json(), tk, ty)


def ohlc_edits(res):
    res['open'] = res['open']['price']
    res['close'] = res['close']['price']
    res['date'] = datetime.now().astimezone(pytz.timezone("America/New_York")).strftime("%Y-%m-%d")
    return [res]


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
    df = pd.DataFrame((ohlc_edits(res) if ty == 'ohlc' else res))
    if ty in {'day', 'ohlc'}:
        df = df[day_price_cols]#.set_index('symbol')
    elif ty == 'intraday-prices':
        df.insert(0, 'symbol', tk)
    
    return df
        


def main():
    return


if __name__ == '__main__':
    main()
