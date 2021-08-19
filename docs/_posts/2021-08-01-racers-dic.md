---
layout: post
title: "racer codes"
---

### r

notebookで作業する

```python
import urllib.request
from bs4 import BeautifulSoup
import json

dic = {}

```

notebookと同じブラウザでcgiページをつくる。辞書へデータを足しこんでいく。

```python

url_oddspark = "https://www.oddspark.com/autorace"
ranking = "/ClassRanking.do?"
S = "term=20210&lgCd=00&rank=S&orderCol=recommend_class_cd&orderDir=asc"
A = "term=20210&lgCd=00&rank=A&orderCol=recommend_class_cd&orderDir=asc"
B = "term=20210&lgCd=00&rank=B&orderCol=recommend_class_cd&orderDir=asc"
opt = "&_rp=687113&page=3" # 2ページ以降はcgiでランダムな番号が振られて生成される

url = url_oddspark + ranking + B + opt

html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "lxml")
links = soup.select("td.racer a")
for link in links:
	racer = "".join(link.text.split())
	cd = link.get("href").strip("/autorace/PlayerDetail.do?playerCd=")
	dic[racer] = cd

```

jsonファイルに書き込み
 
```python

j = json.dumps(dic, ensure_ascii=False)
p = "./racer_codes.json"
with open(p, "w", encoding="utf-8") as f:
  f.write(j)

```

確認

```python
with open(p, "r", encoding="utf-8") as f:
  read_dic = json.load(f)
read_dic
print(len(dic), len(read_dic))
# -> (388, 388)
print(read_dic)
# -> {'青山周平': '3101',
# '鈴木圭一郎': '3206',
# '早川清太郎': '2926', ...
```

### s

```python

racers = ['青山周平', '鈴木圭一郎', '早川清太郎']

detail_url = "https://www.oddspark.com/autorace/PlayerDetail.do?"
cd = read_dic[racers[0]]
url = detail_url + "playerCd=" + cd

soup = s.get_soup(url)
dfs = s.get_dfs(soup)
df = dfs[8]

raps = [rap["競走T"] for i, rap in df.iterrows() if rap["走路  (天候)"][0] == "良"]
raps = [rap for rap in raps if isinstance(rap, float)]
raps = [rap for rap in raps if rap != 0.0]
print(raps)
# -> [3.384, 3.417, 3.409, ...

```