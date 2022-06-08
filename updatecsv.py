from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd
from datetime import datetime
import csv


def get_codes(file_path):
    f = open(file_path, 'r')
    s = f.read()
    return s.split()


def addHeader(code):
    with open("data/" + code + '.csv', 'rt') as f:
        reader = csv.reader(f)
        access_log = [row for row in reader]
        access_log.insert(0, ['Date', 'Close'])
        print(access_log)
        with open("data/" + code + '.csv', 'wt', newline="") as c:
            csvout = csv.writer(c)
            csvout.writerows(access_log)


codes = get_codes("code.txt")
codes = ["6997"]
for code in codes:
    print(code)

    '''
    df_read = pd.read_csv(code+".csv")
    Ldatastr = df_read["datetime"].iloc[-1].split()[0]
    Ldatatime = datetime.strptime(Ldatastr, "%Y-%m-%d")
    now = datetime.today()
    delta = now-Ldatatime
    '''
    my_share = share.Share(code + ".T")
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(
            #share.PERIOD_TYPE_DAY, 20,
            share.PERIOD_TYPE_MONTH, 30,
            share.FREQUENCY_TYPE_DAY,
            1
        )
    except YahooFinanceError as e:
        print(e.message)

    if (symbol_data is None):
        continue

    df = pd.DataFrame({'Date': [datetime.fromtimestamp(d / 1000) for d in symbol_data['timestamp']],\
    'Close' : symbol_data['close']})

    df.to_csv('data/' + code + '.csv', mode='a', index=False)
