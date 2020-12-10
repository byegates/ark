import tabula
import pandas as pd
from datetime import datetime
from google.cloud import storage
import time


cool_down = 1
ip_dir = 'docs/'
op_dir = 'csv/'
prefix = 'pdf/'
f = 'tmp.pdf'
pdf = f"{ip_dir}/{f}"

project_id = 'nw-msds498-ark-etf-analytics'
bucket_name = 'nw-msds498-ark-etf-analytics'
raw_bucket_name = 'nw-msds498-ark-holdings-raw'
storage_client = storage.Client()
bucket = storage_client.get_bucket(bucket_name)
raw_bucket = storage_client.get_bucket(raw_bucket_name)

funds = {
    "ARK_NEXT_GENERATION_INTERNET_ETF_ARKK_HOLDINGS":
        "ARKK",
    "ARK_INNOVATION_ETF_ARKK_HOLDINGS":
        "ARKK",
    "ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS":
        "ARKW",
    "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS":
        "ARKF",
    "ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS":
        "ARKQ",
    "ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS":
        "ARKG",
    "THE_3D_PRINTING_ETF_PRNT_HOLDINGS":
        "PRNT",
    "ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS":
        "IZRL",
    }

rename1 = {"Ticker": "CUSIP"}
rename2 = {
    "Unnamed: 2": "Company", 
    "Unnamed: 4": "Ticker", 
    "Unnamed: 7": "Shares", 
    "Unnamed: 9": "Market_Value", 
    "Unnamed: 10": "Weight"
    }

def dt_f(dt_s, fmt='%m%d%y', to_fmt='%Y-%m-%d'):
    return datetime.strptime(dt_s, fmt).strftime(to_fmt)


cols_to_keep = [nm for nm in rename1] + [nm for nm in rename2]

cols_sorted = ['Date',
 'Fund',
 'Company',
 'Ticker',
 'CUSIP',
 'Shares',
 'Market_Value',
 'Weight']


def pdf_to_csv(f, dt, fund):
    ip = ip_dir + f
    op = op_dir + f"{dt}_{fund}.csv"

    df = tabula.read_pdf(ip, pages="all")[0]
    df = df[cols_to_keep]
    df = df.rename(columns=rename1)
    df = df.rename(columns=rename2)

    df['Date'] = dt
    df['Fund'] = fund
    df['Shares'] = df['Shares'].str.replace(',', '').astype(float)
    df['Market_Value'] = df['Market_Value'].str.replace(',', '').astype(float)

    df[cols_sorted].to_csv(op, index=False)


def parse_blob_name(nm):
    l = nm.strip(prefix).split()
    fund = funds[l[0]]
    _dt = l[1].split('.')[0]
    dt = dt_f(_dt)
    print(f"{fund} @ {dt} for {nm} processed.")
    return dt, fund




def main():
    for blob in raw_bucket.list_blobs(prefix=prefix, delimiter='/'):
        if blob.name != prefix:
            dt, fund = parse_blob_name(blob.name)
            blob.download_to_filename(pdf)
            pdf_to_csv(f, dt, fund)     


if __name__ == "__main__":
    main()