from datetime import datetime
from google.cloud import storage
import urllib.request
from urllib.request import Request, urlopen
import pandas as pd
from io import StringIO
import pytz
import time
import os
import yaml

# set processing time stamp in EST
now = datetime.now()
est_now = now.astimezone(pytz.timezone("America/New_York"))
ts = est_now.strftime("%Y%m%d_%H%M%S_%f")

# configurations
project_id = 'nw-msds498-ark-etf-analytics'
bucket_name = 'nw-msds498-ark-etf-analytics'
raw_bucket_name = 'nw-msds498-ark-holdings-raw'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
raw_bucket = storage_client.get_bucket(raw_bucket_name)

hdr = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36'}

environ = {}

try:
    with open('env.yaml') as f:
        environ = yaml.safe_load(f)
        print('Reading from local env.yaml file...')
        for k, v in environ.items():
            print(f'\'{k}\': \'{v}\'')
        print()
except FileNotFoundError as ffe:
    print('Running on GCP, skip env.yaml file read')

ark_dict = {
    'ARKK': '',
    'ARKQ': '',
    'ARKW': '',
    'ARKG': '',
    'ARKF': '',
    'ARKX': '',
    'PRNT': '',
    'IZRL': '',
    }

def get_env(key):
    try:
        val = os.environ[key]
        print(f"\nENV var: '{key:<15}' value: {val}")
    except KeyError as ke:
        val = environ[key]
    return val


force_pull_raw = True if get_env('FORCE_PULL_RAW') == 'YES' else False
cool_down = int(get_env('COOL_DOWN'))
version = get_env('VERSION')

for k, _ in ark_dict.items():
    ark_dict[k] = get_env(k)

def get_date_from_df(df):
    return datetime.date(df.iloc[0, 0])


def dest_blob_names(etf, asof_date_name):
    dest_blob_nm = f"{asof_date_name}_{etf}.csv"
    raw_dest_blob_nm = f"{asof_date_name}_{etf}_{ts}.csv"
    return dest_blob_nm, raw_dest_blob_nm


def str_to_df(s):
    df = pd.read_csv(StringIO(s))
    df = df[df['ticker'].notna()]
    df.columns = ['Date', 'Fund', 'Company', 'Ticker', 'CUSIP', 'Shares', 'Market_Value', 'Weight']
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def df_to_str(df):
    f = StringIO()
    df.to_csv(f, index=False)
    return f.getvalue()


def retrieve_data(etf, url):
    print(f"\n{etf}:    {url} (retreiving)")
    req = Request(url, headers = hdr)
    raw_str_data = str(urlopen(req).read(), 'utf-8')
    df = str_to_df(raw_str_data)
    asof_date = get_date_from_df(df)
    edited_str_data = df_to_str(df)
    return raw_str_data, edited_str_data, str(asof_date)


def upload_blob(bucket, source_data, blob_name): 
    blob = bucket.blob(blob_name)
    if not blob.exists():
        time.sleep(cool_down) # avoid too frequent update to BigQuery
        print(f"{blob_name}    is being uploaded to (after slept {cool_down} secs):\n    gs://{bucket.name}/{blob_name}")
        blob.upload_from_string(source_data, content_type='text/plain') #'image/jpg'
    else:
        print(f"\n{blob_name}    exists, Upload skipped.")


def ark_pull(dummy):
    for etf, url in ark_dict.items():
        raw_str_data, edited_str_data, asof_date_str = retrieve_data(etf, url)
        dest_blob_nm, raw_dest_blob_nm = dest_blob_names(etf, asof_date_str)

        if bucket.blob(dest_blob_nm).exists() and not force_pull_raw:
            print(f"\n----- {asof_date_str} data was already pulled, BYE -----\n")
            break
        
        upload_blob(raw_bucket, raw_str_data, raw_dest_blob_nm)
        upload_blob(bucket, edited_str_data, dest_blob_nm)

    return 'Success\n\n'


if __name__ == '__main__':
    ark_pull('')
