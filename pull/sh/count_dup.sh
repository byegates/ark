bq query --nouse_legacy_sql --max_rows=100 \
'SELECT
  (
  SELECT
    COUNT(1)
  FROM (
    SELECT
      DISTINCT *
    FROM
      `nw-msds498-ark-etf-analytics`.ark.holdings)) AS distinct_rows,
  (
  SELECT
    COUNT(1)
  FROM
    `nw-msds498-ark-etf-analytics`.ark.holdings) AS total_rows;'
