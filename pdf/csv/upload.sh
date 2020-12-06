bkt=gs://nw-msds498-ark-holdings-raw/trade_price/
files=ARK*.csv
tbl=nw-msds498-ark-etf-analytics:ark.trade_price

for f in $files
do
    gsutil cp $f $bkt
done

# bq rm -f -t $tbl

f=ARK_Trades_20190522_20201111.csv

bq load \
--autodetect \
--source_format=CSV \
$tbl \
$bkt$f
