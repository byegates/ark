# bq rm -f -t 'nw-msds498-ark-etf-analytics:ark.min_price'


FILES=*_min.csv

for f in $FILES
do
    bq load \
    --autodetect \
    --source_format=CSV \
    'nw-msds498-ark-etf-analytics:ark.min_price' \
    "gs://nw-msds498-ark-min-price/$f"
done
