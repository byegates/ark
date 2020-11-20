bq query --nouse_legacy_sql --max_rows=100 \
'SELECT
  DISTINCT dt.Date,
  hd.Fund,
  dt.cnt
FROM (
  SELECT
    Date,
    COUNT(*) AS cnt
  FROM (
    SELECT
      DISTINCT Date,
      Fund
    FROM
      ark.holdings
    ORDER BY
      Date,
      Fund)
  GROUP BY
    Date
  HAVING
    COUNT(*) < 7 ) dt
LEFT JOIN
  ark.holdings hd
ON
  dt.Date = hd.Date
ORDER BY
  Date DESC,
  Fund'
