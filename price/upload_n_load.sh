# for f in `gsutil -m ls  gs://nw-msds498-ark-min-price/ark_min_price*`
bkt=gs://nw-msds498-ark-$1-price/
gsutil -m cp $2 $bkt
# do
    bq load \
    --autodetect \
    --source_format=CSV \
    nw-msds498-ark-etf-analytics:ark.$1_price \
    $bkt$2
# done
