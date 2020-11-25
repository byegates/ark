print(f"{'-'*20} {'core.py':^30} {'-'*20}")

import google.auth
from google.cloud import bigquery, bigquery_storage
from datetime import datetime
import pandas as pd
import pytz
import dash_table.FormatTemplate as FT
from dash_table.Format import Sign, Format

credentials, project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

client = bigquery.Client(credentials=credentials, project=project_id,)
bqsclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

today = datetime.now().strftime("%Y-%m-%d")

def bq_to_df(sql):
    now = datetime.now()
    est_now = now.astimezone(pytz.timezone("America/New_York"))
    ts = est_now.strftime("%Y-%m-%d %H:%M:%S.%f")
    print('-'*50)
    print(ts)
    print(sql)
    return client.query(sql).result().to_dataframe(bqstorage_client=bqsclient)


def all_funds(dt=today):
    print(f"In fucntion all_funds")
    sql = f"""
SELECT
  DISTINCT Fund
FROM
  ark.holdings
ORDER BY
  Fund
    """

    df = bq_to_df(sql)

    return df.Fund.to_list()


def all_tickers(dt=today):
    print(f"In fucntion all_tickers")
    sql = f"""
SELECT
  DISTINCT Ticker
FROM
  ark.holdings
WHERE
  Ticker >= ''
ORDER BY
  Ticker
    """

    df = bq_to_df(sql)

    return df.Ticker.to_list()


def all_dates(dt=today, num=30):
    print(f"In fucntion all_dates")
    sql = f"""
SELECT
  DISTINCT Date
FROM
  ark.holdings
WHERE
  Date <= '{dt}'
ORDER BY
  Date DESC
LIMIT
  {num}
    """

    df = bq_to_df(sql)

    dates = [ v.strftime("%Y-%m-%d") for v in df.Date.to_list()]

    return dates


def edits(df):
    df['weight'] = (df.value/sum(df.value))#.round(8)
    df.insert(0, 'Seq', df.index+1) # Add number sequence of holdings
    return df


def holdings(dt, fd='All', tk='All', use_fd=False, use_tk=True):
    print(f"In fucntion holdings")
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
    dfb.value = dfb0.value - dfb1.value
    dfb['change'] = dfb0.shares / dfb1.shares - 1

    buy = dfb[dfb.shares > 0].sort_values(by='change', ascending=False).reset_index(drop=True)
    sell = dfb[dfb.shares < 0].sort_values(by='change', ascending=True).reset_index(drop=True)
    no_change = dfb[dfb.shares == 0].reset_index(drop=True)

    buy, sell, no_change = set_seq(buy), set_seq(sell), set_seq(no_change)
    new_buy, all_sold = set_seq(new_buy), set_seq(all_sold)

    return buy, sell, no_change, new_buy, all_sold


def compare_position(dt, fund='All', ticker='All', use_fd=False, use_tk=True):
    dates = all_dates(dt)
    dt0, dt1 = dates[0], dates[1]

    df0, df1 = holdings(dt0, fund, ticker, use_fd, use_tk), holdings(dt1, fund, ticker, use_fd, use_tk)

    buy, sell, no_change, new_buy, all_sold = get_diff(df0, df1)

    return buy, sell, no_change, new_buy, all_sold


dates = all_dates()
dt = dates[0]
funds = all_funds(dt)
fund = funds[0]
tickers = all_tickers(dt)

cols = [
        {'name': 'Seq', 'id': 'Seq'},
        {'name': 'Fund', 'id': 'Fund'},
        {'name': 'Ticker', 'id': 'Ticker'},
        {'name': 'Company Name', 'id': 'Company'},
        {'name': 'Shares', 'id': 'shares', 'type': 'numeric', 'format': Format(group=',')},
        {'name': 'Value', 'id': 'value', 'type': 'numeric', 'format': FT.money(2)},
        {'name': 'Weight', 'id': 'weight', 'type': 'numeric', 'format': FT.percentage(6)},
        ]

cols2 = [
        {'name': 'Seq', 'id': 'Seq'},
        {'name': 'Fund', 'id': 'Fund'},
        {'name': 'Ticker', 'id': 'Ticker'},
        {'name': 'Company Name', 'id': 'Company'},
        {'name': 'Shares', 'id': 'shares', 'type': 'numeric', 'format': Format(group=',')},
        {'name': 'Value', 'id': 'value', 'type': 'numeric', 'format': FT.money(2)},
        {'name': 'Change', 'id': 'change', 'type': 'numeric', 'format': FT.percentage(6)},
        ]

right_cols = ['shares', 'value', 'weight', 'change']


def main():
    print(holdings('2020-11-20'))



if __name__ == '__main__':
    main()

