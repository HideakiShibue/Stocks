import shutil
import pandas as pd
import os
import mplfinance as mpf
import math
TORELANCE = [1.02, 40]


def get_codes(file_path):
    f = open(file_path, 'r')
    s = f.read()
    return s.split()


def draw_chart(code, i):

    df = create_dataframe(code)
    if df is False:
        return
    Close = df["close"]
    MA75 = Close.rolling(75).mean()
    MA25 = Close.rolling(25).mean()
    MA200 = Close.rolling(200).mean()
    adds = [
        mpf.make_addplot(MA75[-90:-1], color='b', width=1, alpha=1),
        mpf.make_addplot(MA25[-90:-1], color='y', width=1, alpha=1)
    ]
    mpf.plot(
        df.iloc[-90:-1],
        type='candle',
        datetime_format='%m/%d',
        figsize=(8, 5),
        addplot=adds,
        title=code,
        style='charles',
        savefig=dict(fname="chart/"+str(i)+'.png', dpi=100)
    )


def delete_old_chart():
    shutil.rmtree("chart")

'''
基本的な処理
'''
def create_dataframe(code):
    path = "data/" + code + ".csv"
    if not os.path.isfile(path):
        return False
    df = pd.read_csv(path, index_col='datetime', parse_dates=True)

    # 上場後180日未満のものは取得しない
    if len(df.index) < 180:
        exclude.append(code)
        return False
    
    # 直近のデータがない場合、今後取得しない(上場廃止など)
    if math.isnan(df['volume'].iloc[-1]):  # no data
        exclude.append(code)
        return False

    # 最低取引量
    if df['volume'].iloc[-1] < 10000:
        exclude.append(code)
        return False

    #最低価格(終値で判定)
    if df['close'].iloc[-1] < 40:
        exclude.append(code)
        return False
    return df


matched = []
exclude = []
codes = get_codes("code.txt")

'''
高度な処理(判定アルゴリズム)
'''
for code in codes:
    df = create_dataframe(code)
    if df is False:
        continue
    
    Close = df["close"]
    MA75 = Close.rolling(75).mean()

    # Ma75と終値の近さを判定
    diffp = MA75.iloc[-1]/df["close"].iloc[-1]
    diffabs = MA75.iloc[-1] - df["close"].iloc[-1]
    if diffp > TORELANCE[0] or diffp < 1 or diffabs > TORELANCE[1]:
        continue

    current_slope = MA75.iloc[-1] - MA75.iloc[-2]  # 直近のトレンド
    old_slope = MA75.iloc[-1] - MA75.iloc[-90]  # 過去3ヶ月のトレンド
    if current_slope <= 0 or old_slope >= 0:
        continue

    matched.append(code)

f = open("code_exclude.txt", "w")
f.write("\n".join(exclude))
f.close()
# Graph
for i in range(len(matched)):
    draw_chart(matched[i], i)
