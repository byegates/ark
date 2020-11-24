import pandas as pd
from price import t, weighted_day_price
 
start = datetime(2020, 1, 1)
end = datetime(2020, 11, 23)


def weighted_price_df(r):
    return weighted_day_price(r.open, r.close, r.high, r.low)

res = get_historical_data("TSLA", start, end, token=t)

df = pd.DataFrame(df).T

df.insert(0, 'Ticker', 'TSLA')

df=df.reset_index().rename(columns={"index": 'Date'}).set_index(['Ticker', 'Date'])
# df['weighted_avg'] = df.apply(weighted_price_df, 1).round(2)

df.to_csv('TSLA_2020_hist_price_ytd.csv')

