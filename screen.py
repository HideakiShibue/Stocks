import mplfinance as mpf
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd

TORELANCE = 1.05


def get_codes(file_path):
    f = open('primes.txt', 'r')
    s = f.read()
    return s.split()


def exist_words(text, words):
    exist = False
    for word in words:
        if (word in text):
            exist = True
    return exist


matched = []
codes = get_codes("kabu.xlsx")
for code in codes:
    print(code)
    my_share = share.Share(code + ".T")
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_DAY,
            1,
            share.FREQUENCY_TYPE_DAY,
            1
        )
    except YahooFinanceError as e:
        print(e.message)

    if (symbol_data is None):
        continue

    df = pd.DataFrame(symbol_data)
    df["datetime"] = pd.to_datetime(df.timestamp, unit="ms")
    df.head()

    Close = df["close"]
    MAV75 = Close.rolling(75).mean()
    MAV25 = Close.rolling(25).mean()
    sep = MAV75[-1] / Close[-1]
    if MAV75[-2] > MAV75[-1] or not 1 < sep < TORELANCE:
        continue

    print(sep)
    adds = [
        mpf.make_addplot(MAV75, color='g', width=1, alpha=0.5),
        mpf.make_addplot(MAV25, color='r', width=1, alpha=0.5)
    ]

    mpf.plot(
        df,
        type='line',
        datetime_format='%Y/%m/%d',
        figsize=(20, 5),
        addplot=adds
    )
