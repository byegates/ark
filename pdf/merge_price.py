import pandas as pd
from trade_price import keys, cols0

df1 = pd.read_csv('csv/ARK_Trades_asof_20200521.csv')
df2 = pd.read_csv('csv/ARK_Trades_asof_20201111.csv')

df1['date'] = pd.to_datetime(df1.date)
df2['date'] = pd.to_datetime(df2.date)

df1=df1.sort_values(by=cols0).reset_index(drop=True)
df2=df2.sort_values(by=cols0).reset_index(drop=True)

def compare(df1, df2):
    df1_common = df1[df1.date>='2019-11-12'].set_index(keys)
    df2_common = df2[df2.date<='2020-05-21'].set_index(keys)

    print(f"\n0521 file has {len(df1)} records")
    print(f"1111 file has {len(df2)} records")
    print(f"They share    {len(df1_common)} records")
    print(f"They share    {len(df2_common)} records")

    eq = df1_common.equals(df2_common)

    print(f"Data is {'' if eq else 'in'}consistent between two DFs.")

    if not eq:
        df_chk = df1_common - df2_common

        print(f"\nVerify whats different:")
        print("\nPrice:")
        print(df_chk[df_chk.price != .0])
        print("\nLow:")
        print(df_chk[df_chk.low != .0])
        print("\nHigh:")
        print(df_chk[df_chk.high != .0])
        print("\nClose:")
        print(df_chk[df_chk.close != .0])

    return eq

eq = compare(df1, df2)

if not eq:

    def sel(df, dts=['2020-02-14'], symbols=['TSLA']):
        return df[(df['date'].isin(dts)) & (df['symbol'].isin(symbols))]

    print("\nData in csv/ARK_Trades_asof_20200521.csv:")
    print(sel(df1))
    print("\nData in csv/ARK_Trades_asof_20201111.csv:")
    print(sel(df2))

    null_cols = ['AAPL', 'PYPL', 'CLDR', 'HUYA']
    dts = ['2020-01-23']
    print("\nData in csv/ARK_Trades_asof_20200521.csv:")
    print(sel(df1, dts, null_cols))
    print("\nData in csv/ARK_Trades_asof_20201111.csv:")
    print(sel(df2, dts, null_cols))

    sel1 = (df1['date'] == '2020-02-14') & (df1['symbol'] == 'TSLA')
    sel2 = (df2['date'] == '2020-02-14') & (df2['symbol'] == 'TSLA')
    for col in ['low', 'high', 'close']:
        df2.loc[sel2, col] = float(df1.loc[sel1, col])
    print("\nAfter fix, Data in csv/ARK_Trades_asof_20201111.csv:")
    print(sel(df2))

compare(df1, df2)

#df = pd.concat([df1,df2]).drop_duplicates(keep=False)
df = df2.append(df1[df1.date<'2019-11-12'], ignore_index=True).set_index(keys)
df.to_csv('csv/ARK_Trades_20190522_20201111.csv')