import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates

TORELANCE = 1.05

def get_codes(file_path):
    f = open(file_path, 'r')
    s = f.read()
    return s.split()


def draw_chart(code):
    df = create_dataframe(code)
    plt.plot(df["Close"])
    plt.plot(df["MA200"], color='red')
    plt.plot(df["MA75"], color='blue')
    plt.gcf().autofmt_xdate()


def create_dataframe(code):
    df = pd.read_csv("data/" + code + ".csv", index_col=0, parse_dates=True)
    df.index.name = 'Date'
    print(df)
    Close = df["Close"]
    df["MA75"] = Close.rolling(75).mean()
    df["MA25"] = Close.rolling(25).mean()
    df["MA200"] = Close.rolling(200).mean()
    return df


matched = []
codes = get_codes("code.txt")
for code in codes:
    df = create_dataframe(code)
    flg = True

    if flg is True:
        matched.append(code)


# Graph
plt.figure(figsize=(25, 10))
plt.subplots_adjust(wspace=0.2, hspace=0.1)  # (2)間隔指定

file = 0
while len(matched):
    for j in range(25):
        if len(matched) == 0:
            break
        plt.subplot(5, 5, j+1)  # (3)グラフ描画位置の指定
        draw_chart(matched.pop())
    plt.savefig(f'chart/{file}.png')
    file += 1
