import tabula
import pandas as pd

ip_dir = 'docs/'
op_dir = 'csv/'

files = {
    "ARK_INNOVATION_ETF_ARKK_HOLDINGS 111320.pdf":
        {"Date": '2020-11-13', "Fund": "ARKK"},
    "ARK_INNOVATION_ETF_ARKK_HOLDINGS 111220.pdf":
        {"Date": '2020-11-12', "Fund": "ARKK"},
    "ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS 111320.pdf":
        {"Date": '2020-11-13', "Fund": "ARKW"},
    "ARK_NEXT_GENERATION_INTERNET_ETF_ARKW_HOLDINGS 111220.pdf":
        {"Date": '2020-11-12', "Fund": "ARKW"},
    "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS 111320.pdf":
        {"Date": '2020-11-13', "Fund": "ARKF"},
    "ARK_FINTECH_INNOVATION_ETF_ARKF_HOLDINGS 111220.pdf":
        {"Date": '2020-11-12', "Fund": "ARKF"},
    "ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS 111320.pdf":
        {"Date": '2020-11-13', "Fund": "ARKQ"},
    "ARK_AUTONOMOUS_TECHNOLOGY_&_ROBOTICS_ETF_ARKQ_HOLDINGS 111220.pdf":
        {"Date": '2020-11-12', "Fund": "ARKQ"},
    "ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS 111320.pdf":
        {"Date": '2020-11-13', "Fund": "ARKG"},
    "ARK_GENOMIC_REVOLUTION_MULTISECTOR_ETF_ARKG_HOLDINGS 111220.pdf":
        {"Date": '2020-11-12', "Fund": "ARKG"},
    "THE_3D_PRINTING_ETF_PRNT_HOLDINGS 111320.pdf":
        {"Date": '2020-11-13', "Fund": "PRNT"},
    "THE_3D_PRINTING_ETF_PRNT_HOLDINGS 111220.pdf":
        {"Date": '2020-11-12', "Fund": "PRNT"},
    "ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS 111320.pdf":
        {"Date": '2020-11-13', "Fund": "IZRL"},
    "ARK_ISRAEL_INNOVATIVE_TECHNOLOGY_ETF_IZRL_HOLDINGS 111220.pdf":
        {"Date": '2020-11-12', "Fund": "IZRL"},
    }

rename1 = {"Ticker": "CUSIP"}
rename2 = {
    "Unnamed: 2": "Company", 
    "Unnamed: 4": "Ticker", 
    "Unnamed: 7": "Shares", 
    "Unnamed: 9": "Market_Value", 
    "Unnamed: 10": "Weight"
    }

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



def main():
    for f, v in files.items():
        pdf_to_csv(f, v['Date'], v['Fund'])


if __name__ == "__main__":
    main()