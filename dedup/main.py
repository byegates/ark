from google.cloud import bigquery
import time

def dup_exist(client, tbl):
    query = f"""
        SELECT
      (
      SELECT
        COUNT(1)
      FROM (
        SELECT
          DISTINCT *
        FROM
          {tbl})) AS distinct_rows,
      (
      SELECT
        COUNT(1)
      FROM
        {tbl}) AS total_rows
    """

    query_job = client.query(query)

    for row in query_job:
        print(f"\ndistinct_rows : {row['distinct_rows']} rows found in table: {tbl}")
        print(f"total_rows    : {row['total_rows']} rows found in table: {tbl}\n")
        return True if row['distinct_rows'] < row['total_rows'] else False

    return


def dedup_func(client, tbl):
    query = f"""
    CREATE OR REPLACE TABLE
        {tbl} AS
    SELECT
        DISTINCT *
    FROM
        {tbl}
    ORDER BY
        Date DESC,
        Fund
    """

    print("DeDup Function Started...")
    client.query(query)
    print("DeDup Function Completed...")
    time.sleep(2)

    return


def dedup(tbl, dummy):
    print(f"Deduping table: {tbl}")
    client = bigquery.Client()

    if dup_exist(client, tbl):
        dedup_func(client, tbl)
        dup_exist(client, tbl)

    return 'Success\n\n'


if __name__ == '__main__':
    dedup('ark.holdings', '')
