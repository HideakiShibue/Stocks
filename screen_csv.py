import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import os
TORELANCE = 1.02


def get_codes(file_path):
    f = open(file_path, 'r')
    s = f.read()
    return s.split()


def draw_chart(code):
    df = create_dataframe(code)
    df = df.head(120)
    plt.plot(df["Close"])
    plt.plot(df["MA200"], color='red')
    plt.plot(df["MA75"], color='blue')
    plt.gcf().autofmt_xdate()


def create_dataframe(code):
    if not os.path.isfile("data/" + code + ".csv"):
        return False
    df = pd.read_csv("data/" + code + ".csv", index_col=0, parse_dates=True)
    df.index.name = 'Date'
    print(code)
    if len(df.index) < 100:
        return False
    Close = df["Close"]
    df["MA75"] = Close.rolling(75).mean()
    df["MA25"] = Close.rolling(25).mean()
    df["MA200"] = Close.rolling(200).mean()
    return df


matched = []
codes = get_codes("code.txt")
for code in codes:
    df = create_dataframe(code)
    if df is False:
        continue
    diff = df["MA75"].iloc[-1]/df["Close"].iloc[-1]
    if diff > TORELANCE or 1/diff > TORELANCE:
        continue

    current_slope = df["MA75"].iloc[-1] - df["MA75"].iloc[-2]  # 直近の上昇
    old_slope = df["MA75"].iloc[-1] - df["MA75"].iloc[-90]  # 過去の下落
    if current_slope < 0 or old_slope > 0:
        continue

    matched.append(code)


# Graph

file = 0
while len(matched):
    plt.clf()
    plt.figure(figsize=(25, 10))
    plt.subplots_adjust(wspace=0.2, hspace=0.1)  # (2)間隔指定
    
    for j in range(25):
        if len(matched) == 0:
            break
        plt.subplot(5, 5, j+1)  # (3)グラフ描画位置の指定
        draw_chart(matched.pop())
    plt.savefig(f'chart/{file}.png')
    file += 1

