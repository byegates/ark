for f in `gsutil -m ls  gs://nw-msds498-ark-min-price/ark_min_price*`
do
    bq load \
    --autodetect \
    --source_format=CSV \
    'nw-msds498-ark-etf-analytics:ark.min_price1' \
    $f
done
