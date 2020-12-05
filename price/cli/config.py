import yaml
from google.cloud import bigquery
from datetime import datetime
import pytz


with open('api.yaml') as f:
    api = yaml.load(f, Loader=yaml.FullLoader)

symbols_to_skip = set(
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

stand_ty = { # standard request types
    'quote', # 1 real time is available 24x7, ohlc info available around 8:11 PM?
    'ohlc', # 1, available # 8 PM EST?
    'intraday-prices', # 50 msgs
    'price-target', # require accesses?
}

u, t = api['iex']['u'], api['iex']['t']

day_price_cols = ['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']

errors = {
    b'Unknown symbol',
    b'{}',
    b'[]',
    b'You have supplied invalid values for this request',
}

client = bigquery.Client()


def est_now():
    return datetime.now().astimezone(pytz.timezone("America/New_York"))


today = est_now().strftime("%Y-%m-%d")

def bq_to_df(sql):
    ts = est_now().strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{'-'*50}\n{ts}\n{sql}")
    return client.query(sql).to_dataframe()


def query(field='Ticker', dt=today, num=30):
    sql = f"""
SELECT
  DISTINCT {field}
FROM
  ark.holdings
  {"WHERE Ticker >= ''" if field == 'Ticker' else ''}
  {f"WHERE Date <= '{dt}'" if field == 'Date' else ''}
ORDER BY
  {field} {'DESC' if field == 'Date' else ''}
  {f'LIMIT {num}' if field == 'Date' else ''} """

    lst = bq_to_df(sql)[field].to_list()

    return [v.strftime("%Y-%m-%d") for v in lst] if field == 'Date' else lst


dates = query('Date')
symbols = query('Ticker')
