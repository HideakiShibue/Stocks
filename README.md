# 説明

## 使い方

```bash
git clone https://github.com/ShutaShibue/Stocks.git
```

を実行して、pythonファイル等がある階層に
/data フォルダ
/chart フォルダ
code_exlude.txt ファイルを作る

``` bash
pip install -r requirements.txt
```

を実行して、必要なライブラリをインストール

## updatecsv.py

タスクスケジューラーで毎日夜に実行させるべきだが、まだやってない  
エラー処理がうまく行っていないが、動かないことはない
基本的にはcode.txtに必要な銘柄の銘柄コードを書いて(1行1銘柄)実行

## screen_csv.py

このファイルに判定アルゴリズムを書く。
現状は75日線と直近終値が近く、中期の下げが終わって上向きつつある銘柄を選ぶようなアルゴリズムを実装してある
