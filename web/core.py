import google.auth
from google.cloud import bigquery, bigquery_storage
from datetime import datetime
import pandas as pd


credentials, project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

client = bigquery.Client(credentials=credentials, project=project_id,)
bqsclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

today = datetime.now().strftime("%Y-%m-%d")

def bq_to_df(sql):
    return client.query(sql).result().to_dataframe(bqstorage_client=bqsclient)


def trade_dates(dt=today, num=5):
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


def holdings_by_date_fund_formatted(dt, fund='ARKK'):
    sql = f"""
SELECT
  Ticker,
  Date,
  FORMAT("%'15.10d", CAST(SUM(Shares) AS INT64)) AS shares,
  CONCAT('$ ', FORMAT("%'17.2f", SUM(Market_Value))) AS value
FROM
  ark.holdings
WHERE
  Date = '{dt}'
  AND fund = '{fund}'
GROUP BY
  Ticker,
  Date
ORDER BY
  SUM(Market_Value) DESC    """

    return client.query(sql).result().to_dataframe(bqstorage_client=bqsclient)


def holdings_by_date_fund(dt, fund='ARKK'):
    sql = f"""
SELECT
  *
FROM
  ark.holdings
WHERE
  Date = '{dt}'
  AND fund = '{fund}'
ORDER BY
  Market_Value DESC    """

    return client.query(sql).result().to_dataframe(bqstorage_client=bqsclient)


def holdings_by_date(dt):
    sql = f"""
SELECT
  Ticker,
  Company,
  FORMAT("%'d", CAST(SUM(Shares) AS INT64)) AS shares,
  CONCAT('$ ', FORMAT("%'.2f", SUM(Market_Value))) AS value
FROM
  ark.holdings
WHERE
  Date = '{dt}'
GROUP BY
  Ticker,
  Company
ORDER BY
  SUM(Market_Value) DESC
    """

    return client.query(sql).result().to_dataframe(bqstorage_client=bqsclient)


def holdings_overall(cur_dt):
    df = holdings_by_date(cur_dt)
    val_float = df.value.str.strip('$ ').str.replace(',', '').astype(float)
    df['weight'] = (val_float/sum(val_float)).round(8)
    df.insert(0, 'Seq', df.index+1) # Add number sequence of holdings
    return df


def main():
    #cur_dt, pri_dt = get_two_latest_dates()
    print(holdings_by_date('2020-11-20'))



if __name__ == '__main__':
    main()

