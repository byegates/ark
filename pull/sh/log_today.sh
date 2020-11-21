if [ $# -eq 0 ]
  then
    dt=date +%Y-%m-%d
    tm="00:00:00.000"
else
    dt=$1
    tm=$2
fi

gcloud functions logs read ark-holdings-daily-pull \
--limit 1000 \
--start-time="$dt $tm"
