from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd
import openpyxl
from datetime import date, datetime


def get_codes(file_path):
    skip_words = ['ETF・ETN', 'PRO Market']
    codes = []

    wb = openpyxl.load_workbook(file_path)
    ws = wb["Sheet1"]
    for row in ws.iter_rows(min_row=2):
        market = str(row[3].value)
        if (not exist_words(market, skip_words)):
            codes.append(str(row[1].value))
    return codes


def exist_words(text, words):
    exist = False
    for word in words:
        if (word in text):
            exist = True
    return exist


codes = get_codes("kabu.xlsx")
for code in ["6997"]:
    print(code)
    
    df_read = pd.read_csv(code+".csv")
    Ldatastr = df_read["datetime"].iloc[-1].split()[0]
    Ldatatime = datetime.strptime(Ldatastr, "%Y-%m-%d")
    now = datetime.today()
    delta = now-Ldatatime

    my_share = share.Share(code + ".T")
    symbol_data = None

    try:
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_DAY,
            delta.days-1,
            share.FREQUENCY_TYPE_DAY,
            1
        )
    except YahooFinanceError as e:
        print(e.message)

    if (symbol_data is None):
        continue

    df = pd.DataFrame({'datetime': [datetime.fromtimestamp(d / 1000) for d in symbol_data['timestamp']],\
    'close' : symbol_data['close']})

    df.to_csv(code + '.csv', mode='a', header=False, index=False)
