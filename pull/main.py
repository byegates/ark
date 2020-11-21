from datetime import datetime
from google.cloud import storage
import urllib.request
from urllib.request import Request, urlopen
import pandas as pd
from io import StringIO
import pytz
import time
import os

# Active ETFs
arkk_url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_INNOVATION_ETF_ARKK_HOLDINGS.csv'
arkq_url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS.csv'
arkw_url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS.csv'
arkg_url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS.csv'
arkf_url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS.csv'
# Index ETFs
prnt_url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/THE_3D_PRINTING_ETF_PRNT_HOLDINGS.csv'
izrl_url = 'https://ark-funds.com/wp-content/fundsiteliterature/csv/ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS.csv'

ark_dict = {
    'ARKK': arkk_url,
    'ARKQ': arkq_url,
    'ARKW': arkw_url,
    'ARKG': arkg_url,
    'ARKF': arkf_url,
    'PRNT': prnt_url,
    'IZRL': izrl_url,
    }

now = datetime.now()
est_now = now.astimezone(pytz.timezone("America/New_York"))
ts = est_now.strftime("%Y%m%d_%H%M%S_%f")

project_id = 'nw-msds498-ark-etf-analytics'
bucket_name = 'nw-msds498-ark-etf-analytics'
raw_bucket_name = 'nw-msds498-ark-holdings-raw'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
raw_bucket = storage_client.get_bucket(raw_bucket_name)

hdr = {'User-Agent': 'Mozilla/5.0'}

environ = {
    'COOL_DOWN': '2',
    'FORCE_PULL_RAW': 'NO',
    'VERSION': 'NA'
}

def get_env(key):
    try:
        val = os.environ[key]
        print(f"\nENV var: '{key:<15}' value: {val}")
    except KeyError as ke:
        print(f"\nENV var: '{key:<15}' value: {environ[key]:<5} (default)")
        val = environ[key]
    return val


force_pull_raw = True if get_env('FORCE_PULL_RAW') == 'YES' else False
cool_down = int(get_env('COOL_DOWN'))
version = get_env('VERSION')


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
    req = Request(url, headers=hdr)
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
