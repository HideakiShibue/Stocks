import os
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


def update(codes, excludes):

    while len(codes):
        code = codes.pop()
        if code in excludes:
            continue
        print(code)
        path = "data/" + code + ".csv"
        new = False if os.path.isfile(path) else True

        if not new:
            df_read = pd.read_csv(path)
            Ldatastr = df_read["datetime"].iloc[-1].split()[0]
            Ldatatime = datetime.strptime(Ldatastr, "%Y-%m-%d")
            today = datetime.today()
            delta = int(str(today-Ldatatime).split()[0])

        my_share = share.Share(code + ".T")
        symbol_data = None

        try:
            if new:
                symbol_data = my_share.get_historical(
                    share.PERIOD_TYPE_MONTH, 30,
                    share.FREQUENCY_TYPE_DAY, 1
                )
            elif delta > 1:
                symbol_data = my_share.get_historical(
                    share.PERIOD_TYPE_DAY, delta,
                    share.FREQUENCY_TYPE_DAY, 1
                )

        except YahooFinanceError as e:
            print(e.message)

        if (symbol_data is None):
            continue

        df = pd.DataFrame({
            'datetime':
                [datetime.fromtimestamp(d/1000) for d in symbol_data['timestamp']],
            'open': symbol_data['open'],
            'high': symbol_data['high'],
            'low': symbol_data['low'],
            'close': symbol_data['close'],
            'volume': symbol_data['volume']
            })

        # if not updated
        lastdata = (df['datetime'].iloc[-1])

        # drop incomplete data
        time = str(lastdata).split()
        if time[1] != "09:00:00":
            ind = df.index[-1]
            df.drop(ind, axis=0, inplace=True)

        if new:
            df.to_csv(path, index=False)
        else:
            df.to_csv(path, mode='a', header=None, index=False)


codes = get_codes("code.txt")
excludes = get_codes("code_exclude.txt")
try:
    update(codes, excludes)
except KeyboardInterrupt:
    update(codes, excludes)

# add excludes
excludes.append("")
