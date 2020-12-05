find . -type f -name "*.csv" | while read fname; do
    dirname=`dirname "$fname"`
    filename=`basename "$fname"`
    IFS='_' read -ra ADDR <<< "$filename"
    newname="${ADDR[0]}_20201124_20201125.csv"
    mv "${dirname}/$filename" "${dirname}/$newname"
done
