bq mkdef \
--autodetect \
--source_format=CSV \
"gs://nw-msds498-ark-day-price/nw-msds498-ark-day-price/AAPL_2020_hist_price_ytd.csv" > \
'day_price.json'
