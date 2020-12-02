bq rm -f -t 'nw-msds498-ark-etf-analytics:ark.day_price'

FILES=*_2020_hist_price_ytd.csv

for f in $FILES
do
    bq load \
    --autodetect \
    --source_format=CSV \
    'nw-msds498-ark-etf-analytics:ark.day_price' \
    "gs://nw-msds498-ark-day-price/$f"
done
