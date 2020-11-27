bq rm -f -t 'nw-msds498-ark-etf-analytics:ark.min_price'


bq load \
--autodetect \
--source_format=CSV \
'nw-msds498-ark-etf-analytics:ark.min_price' \
"gs://nw-msds498-ark-min-price/AAPL_2020-11-24_min.csv"


#FILES=*_2020_hist_price_ytd.csv
#
#for f in $FILES
#do
#    bq load \
#    --autodetect \
#    --source_format=CSV \
##    'nw-msds498-ark-etf-analytics:ark.min_price' \
#    "gs://nw-msds498-ark-day-price/$f"
#done
