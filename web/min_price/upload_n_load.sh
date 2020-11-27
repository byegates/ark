f="TSLA_2020-11-25_min.csv"

gsutil -m cp $f gs://nw-msds498-ark-min-price/

bq rm -f -t 'nw-msds498-ark-etf-analytics:ark.min_price'

bq load \
--autodetect \
--source_format=CSV \
'nw-msds498-ark-etf-analytics:ark.min_price' \
"gs://nw-msds498-ark-min-price/$f"
