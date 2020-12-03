# bq rm -f -t 'nw-msds498-ark-etf-analytics:ark.day_price'

FILES=*_20201124_25.csv

for f in $FILES
do
    gsutil -m cp $f gs://nw-msds498-ark-day-price/
    bq load \
    --autodetect \
    --source_format=CSV \
    'nw-msds498-ark-etf-analytics:ark.day_price' \
    "gs://nw-msds498-ark-day-price/$f"
done
