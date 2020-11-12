cat /etc/os-release

sudo apt-get update
sudo apt-get upgrade

# Building python 3.8.6
sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev curl libbz2-dev
curl -O https://www.python.org/ftp/python/3.8.6/Python-3.8.6.tar.xz
tar -xf Python-3.8.6.tar.xz
cd Python-3.8.6/
./configure --enable-optimizations --enable-loadable-sqlite-extensions
make -j 4
sudo make install
python3 -m pip install -U pip
# sudo make altinstall

sudo apt-get install python3-venv
python3 -m venv ~/.ark
source ~/.ark/bin/activate
pip3 install google-cloud-core -U
pip3 install google-cloud-storage -U
pip3 install google-cloud-bigquery -U
pip3 install pandas -U
pip3 freeze > requirements.txt

curl -X POST "https://us-central1-nw-msds498-ark-etf-analytics.cloudfunctions.net/ark-holdings-daily-pull" -H "Content-Type: application/json" --data "{}"
curl -O https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv 

curl https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv > ARKK_20201009.csv

gcloud config set project nw-msds498-ark-etf-analytics
gcloud config set project msds-498-group-project

pip3 install google-cloud-datastore -U

OAuth client created
39160422190-r3l5qtd444lg4k99eo0bm4biq730h8v9.apps.googleusercontent.com
znXUUfTJ1pvbd3sNATZ_jWYO

cd ~
cd gcf-gmail-codelab/auth

# Deploy Cloud Function auth_init
gcloud functions deploy auth_init --runtime=nodejs8 --trigger-http --env-vars-file=env_vars.yaml

# Deploy Cloud Function auth_callback
gcloud functions deploy auth_callback --runtime=nodejs8 --trigger-http --env-vars-file=env_vars.yaml

l
gcloud functions logs read
gsutil ls -l 'gs://nw-msds498-ark-etf-analytics/2020-11-02*' | sort -k 2
gsutil ls -l 'gs://nw-msds498-ark-holdings-raw/2020-11-02*' | sort -k 2
gsutil -m rm 'gs://nw-msds498-ark-holdings-raw/2020-11-02*'

gsutil cp dummy gs://nw-msds498-ark-etf-analytics/edited/dummy
gsutil mb gs://nw-msds498-ark-etf-analytics-raw
gsutil -m mv 'gs://nw-msds498-ark-etf-analytics/2020*' gs://nw-msds498-ark-holdings-raw
gsutil -m mv 'gs://nw-msds498-ark-etf-analytics/edited/*' gs://nw-msds498-ark-etf-analytics

gsutil ls -l gs://nw-msds498-ark-etf-analytics

--New Buckets
gsutil mb gs://nw-msds498-ark-holdings-raw
gsutil mb gs://nw-msds498-ark-trades


-- BigQuery
bq rm -f -t nw-msds498-ark-etf-analytics:ark.holdings
bq mk -t ark.holdings Date:DATE,Fund:STRING,Company:STRING,Ticker:STRING,CUSIP:STRING,Shares:FLOAT,Market_Value:FLOAT,Weight:FLOAT

bq rm -f -t nw-msds498-ark-etf-analytics:ark.trades
bq mk --external_table_definition=~/ark/data/tmp/trades_config.json ark.trades 

bq show \
--schema \
--format=prettyjson \
nw-msds498-ark-etf-analytics:ark.trades > ~/ark/data/tmp/trades_schema.json

bq show \
--format=prettyjson \
nw-msds498-ark-etf-analytics:ark.trades > ~/ark/data/tmp/trades_config.json

-- Deloy cloud functions
gcloud functions deploy csv_loader \
--runtime=python38 \
--trigger-resource=gs://nw-msds498-ark-etf-analytics \
--trigger-event=google.storage.object.finalize \
--entry-point=csv_loader \
--env-vars-file=env.yaml

gcloud functions describe ark-holdings-daily-pull
gcloud functions deploy ark-holdings-daily-pull \
--runtime=python38 \
--trigger-http \
--allow-unauthenticated \
--entry-point=ark_pull \
--env-vars-file=env.yaml

# http-pull trigger url
# https://us-central1-nw-msds498-ark-etf-analytics.cloudfunctions.net/ark-holdings-daily-pull

curl -X POST https://us-central1-nw-msds498-ark-etf-analytics.cloudfunctions.net/ark-holdings-daily-pull -H "Content-Type:application/json"  -d '{}'


Enable venv:
sudo apt-get install python3-venv
python3 -m venv ~/.csv_loader
source ~/.csv_loader/bin/activate
pip3 install google-cloud-bigquery -U


source ~/.msds498GroupProject/bin/activate

Create new remote repo from existing local repo:
git remote add origin git@github.com:byegates/ark.git
git pull origin master --allow-unrelated-histories
git merge master

gcloud iam service-accounts keys create ~/key.json  --iam-account ark-pull@nw-msds498-ark-etf-analytics.iam.gserviceaccount.com
echo "" >> .gitignore
echo "# ignore key file which was used for dev/ut/debug" >> .gitignore
echo "pull/key.json" >> .gitignore


## Compute
gcloud projects list
gcloud functions list
gcloud components list

gcloud compute instances list

gcloud compute instances update frontend-default-40682 --no-deletion-protection --zone asia-east2-c
gcloud compute instances update jenkins-default-5066 --no-deletion-protection --zone asia-east2-c

gcloud compute instances delete jenkins-default-5066 --zone asia-east2-c
gcloud compute instances delete frontend-default-40682 --zone asia-east2-c


## Mac python version management
https://opensource.com/article/19/5/python-3-default-mac

## pyenv virtual env management
https://realpython.com/intro-to-pyenv/