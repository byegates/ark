for var in "$@"
do
    echo "--------------"
    echo "Fixing $var"
    echo "Downloading..."
    gsutil cp gs://nw-msds498-ark-etf-analytics/$var ./
    echo "Uploading  ..."
    gsutil cp ./$var gs://nw-msds498-ark-etf-analytics/
    echo "Done"
done
