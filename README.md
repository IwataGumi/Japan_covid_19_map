# 都道府県別の新型コロナデータアプリ

![japancovid19map-fptjq8vdssb5kmxsmk3oka streamlit app_](https://github.com/IwataGumi/Japan_covid_19_map/assets/70084358/319fced9-e7e3-4f34-a4e3-fb85397437a8)
指定した期間の総感染者数の分布を表示するデータアプリケーションです。

[Zenn記事](https://zenn.dev/hekuchandao/articles/e6b57ff3730fb4)

# Install
## Poetry
1. Run poetry install
```
poetry install
```
2. Run the application
```
poetry run python -m streamlit run main.py
```

## Normal
1. Install dependencies
```
pip install -r requirements.txt
```
2. Run app
```
streamlit run main.py
```

# その他
geojsonは国土交通省 国土地理院の [地球地図日本](https://www.gsi.go.jp/kankyochiri/gm_jpn.html) で公開しているデータを加工して使用しています。
感染者数のデータは[オープンデータ｜厚生労働省](https://www.mhlw.go.jp/stf/covid-19/open-data.html)から持ってきています。
