f="ark_min_price_2020-0$1.csv"

gsutil -m cp $f gs://nw-msds498-ark-min-price/

bq load \
--autodetect \
--source_format=CSV \
'nw-msds498-ark-etf-analytics:ark.min_price' \
"gs://nw-msds498-ark-min-price/$f"
