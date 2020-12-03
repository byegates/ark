import google.auth
from google.cloud import bigquery
from datetime import datetime
import pandas as pd
import pytz
import dash_table.FormatTemplate as FT
from dash_table.Format import Sign, Format

client = bigquery.Client()
today = datetime.now().strftime("%Y-%m-%d")


def bq_to_df(sql):
    est_now = datetime.now().astimezone(pytz.timezone("America/New_York"))
    ts = est_now.strftime("%Y-%m-%d %H:%M:%S.%f")
    print(f"{'-'*50}\n{ts}\n{sql}")
    return client.query(sql).to_dataframe()


def query(field='Ticker', dt=today, num=99):
    sql = f"""
SELECT
  DISTINCT {field}
FROM
  ark.holdings
  {"WHERE Ticker >= ''" if field == 'Ticker' else ''}
  {f"WHERE Date <= '{dt}'" if field == 'Date' else ''}
ORDER BY
  {field} {'DESC' if field == 'Date' else ''}
  {f'LIMIT {num}' if field == 'Date' else ''}
    """

    df = bq_to_df(sql)
    lst = df[field].to_list()

    return [v.strftime("%Y-%m-%d") for v in lst] if field == 'Date' else lst


def estimate_trade_price(r):
    return r['close_price']

def edits(df):
    df['weight'] = (df.value/sum(df.value))
    df['close_price'] = (df.value/df.shares)
    df['trade_price'] = df.apply(estimate_trade_price, axis=1)
    df.insert(0, 'Seq', df.index+1) # Add number sequence of holdings
    return df


def holdings(dt, fd='All', tk='All', use_fd=False, use_tk=True):
    sql = f"""
SELECT
  {f"Fund, " if use_fd else ''}
  {f"Ticker, " if use_tk  else ''}
  Company,
  CAST(SUM(Shares) AS INT64) AS shares,
  SUM(Market_Value) AS value
FROM
  ark.holdings
WHERE
  Date = '{dt}'
  {f"AND fund = '{fd}'" if fd != 'All' else ''}
  {f"AND Ticker = '{tk}'" if tk != 'All' else ''}
GROUP BY
  {f"Fund, " if use_fd else ''}
  {f"Ticker, " if use_tk  else ''}
  Company
ORDER BY
  SUM(Market_Value) DESC    """

    return edits(bq_to_df(sql))


def set_seq(df):
    df.Seq = df.index + 1
    return df


def get_diff(df0, df1):
    set0 = set(df0.Ticker.to_list())
    set1 = set(df1.Ticker.to_list())

    new_buy = set0 - set1
    all_sold = set1 - set0
    both = set0 & set1

    new_buy = df0[df0.Ticker.isin(new_buy)].sort_values(by='shares', ascending=False).reset_index(drop=True)
    all_sold = df0[df0.Ticker.isin(all_sold)].sort_values(by='shares', ascending=False).reset_index(drop=True)

    dfb = df0[df0.Ticker.isin(both)].sort_values(by='Ticker').reset_index(drop=True)
    dfb0 = dfb.copy(deep=True)
    dfb1 = df1[df1.Ticker.isin(both)].sort_values(by='Ticker').reset_index(drop=True)

    dfb.shares = dfb0.shares - dfb1.shares
    dfb.value = dfb.shares * dfb0['trade_price']
    dfb['change'] = dfb0.shares / dfb1.shares - 1

    buy = dfb[dfb.shares > 0].sort_values(by='value', ascending=False).reset_index(drop=True)
    sell = dfb[dfb.shares < 0].sort_values(by='value', ascending=True).reset_index(drop=True)
    no_change = dfb[dfb.shares == 0].reset_index(drop=True)

    buy, sell, no_change = set_seq(buy), set_seq(sell), set_seq(no_change)
    new_buy, all_sold = set_seq(new_buy), set_seq(all_sold)

    return buy, sell, no_change, new_buy, all_sold


def compare_position(dt, fund='All', ticker='All', use_fd=False, use_tk=True):
    dates = query(field='Date', dt=dt, num=2)
    dt0, dt1 = dates[0], dates[1]

    df0, df1 = holdings(dt0, fund, ticker, use_fd, use_tk), holdings(dt1, fund, ticker, use_fd, use_tk)

    buy, sell, no_change, new_buy, all_sold = get_diff(df0, df1)

    return buy, sell, no_change, new_buy, all_sold


dates = query('Date')
tickers = query('Ticker')
funds = query('Fund')
dt = dates[0]
fund = funds[0]

cols = [
        {'name': 'Seq', 'id': 'Seq'},
        {'name': 'Fund', 'id': 'Fund'},
        {'name': 'Ticker', 'id': 'Ticker'},
        {'name': 'Company Name', 'id': 'Company'},
        {'name': 'Shares', 'id': 'shares', 'type': 'numeric', 'format': Format(group=',')},
        {'name': 'Value', 'id': 'value', 'type': 'numeric', 'format': FT.money(2)},
        {'name': 'Close Price', 'id': 'close_price', 'type': 'numeric', 'format': FT.money(2)},
        {'name': 'Weight', 'id': 'weight', 'type': 'numeric', 'format': FT.percentage(6)},
        ]

cols2 = [
        {'name': 'Seq', 'id': 'Seq'},
        {'name': 'Fund', 'id': 'Fund'},
        {'name': 'Ticker', 'id': 'Ticker'},
        {'name': 'Company Name', 'id': 'Company'},
        {'name': 'Shares', 'id': 'shares', 'type': 'numeric', 'format': Format(group=',')},
        {'name': 'Trade Size*', 'id': 'value', 'type': 'numeric', 'format': FT.money(2)},
        {'name': 'Trade Price**', 'id': 'trade_price', 'type': 'numeric', 'format': FT.money(2)},
        {'name': 'Close Price', 'id': 'close_price', 'type': 'numeric', 'format': FT.money(2)},
        {'name': 'Change', 'id': 'change', 'type': 'numeric', 'format': FT.percentage(6)},
        ]

right_cols = ['shares', 'value', 'weight', 'change', 'close_price', 'trade_price']


def main():
    print(holdings('2020-11-20'))



if __name__ == '__main__':
    main()

