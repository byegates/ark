import google.auth
from google.cloud import bigquery, bigquery_storage
from datetime import datetime
import pandas as pd
#import cdata.googlebigquery as mod


credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

# Make clients.
bqclient = bigquery.Client(credentials=credentials, project=your_project_id,)
bqstorageclient = bigquery_storage.BigQueryReadClient(credentials=credentials)

client = bigquery.Client()

#cnxn = mod.connect("""DataSetId=ark;
#    ProjectId=nw-msds498-ark-etf-analytics;
#    InitiateOAuth=GETANDREFRESH;
#    OAuthSettingsLocation=/PATH/TO/OAuthSettings.txt""")


def get_all_dates():
    sql = f"""
SELECT
  DISTINCT Date
FROM
  ark.holdings
ORDER BY
  Date DESC
    """

    query_job = client.query(sql)
    results = query_job.result()

    dates = [ row.Date.strftime("%Y-%m-%d") for row in results]

    return dates


def get_two_latest_dates(dt=None):
    if dt is None:
        where = ''
    else:
        where = f"""
WHERE
  Date <= '{dt}'
        """

    sql = f"""
SELECT
  DISTINCT Date
FROM
  ark.holdings
{where}
ORDER BY
  Date DESC
LIMIT
  2
    """

    query_job = client.query(sql)
    results = query_job.result()

    dates = [ row.Date.strftime("%Y-%m-%d") for row in results]
    cur_dt = dates[0]
    pri_dt = dates[1]

    return cur_dt, pri_dt


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

    df = bqclient.query(sql).result().to_dataframe(bqstorage_client=bqstorageclient)
    return df


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

    df = bqclient.query(sql).result().to_dataframe(bqstorage_client=bqstorageclient)
    return df


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

    df = bqclient.query(sql).result().to_dataframe(bqstorage_client=bqstorageclient)
    return df


def main():
    #cur_dt, pri_dt = get_two_latest_dates()
    print(holdings_by_date('2020-11-20'))



if __name__ == '__main__':
    main()

