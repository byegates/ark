#from iexfinance.refdata import get_symbols
from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from datetime import datetime


u1 = 'https://cloud.iexapis.com/stable/stock/'
u0 = 'https://sandbox.iexapis.com/stable/stock/'
test_token = 'Tpk_e2d85eb6c1ec4a3ab62d4e4a4ed8b22c'
cur_dt = datetime.today().strftime('%Y-%m-%d')

o = 'open'
h = 'high'
l = 'low'
c = 'close'


def get_token(fi='dont.mess.with.me'):
    with open(fi, 'r') as f:
        return f.readline().strip()


t = get_token()
#get_symbols(output_format='pandas', token=token)



def chart_by_day_url(ticker, dt):
    return f"{u0}{ticker}/chart/date/{dt}?chartByDay=true&token={token}"


def weighted_day_price(o, c, h, l):
    return .3*o + .3*c + .2*h + .2*l


def estimate_price_by_day(ticker, dt):
    """To be Added"""
    ticker = ticker.upper()
    res = get_historical_data(ticker, dt.replace('-', ''), token=t)
    if res[ticker]['chart'] == []:
        return None
    else:
        r = res[dt]
        return weighted_day_price(r[o], r[c], r[h], r[l])


def quote(ticker):
    s = Stock(ticker, token=t)


def main():
    return


if __name__ == '__main__':
    main('')
