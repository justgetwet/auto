import numpy as np
import pandas as pd
import re
import json
import datetime
import copy
import seaborn as sns
from racers import Racers
# pd.set_option('display.max_columns', 22)
# from race import Scrape, RaceUrls
from racers import Racers

# url_racelist = url_oddspark + "/RaceList.do?"
# url_odds = url_oddspark + "/Odds.do?"
# url_pred = url_oddspark + "/yosou"
# url_result = url_oddspark + "/RaceResult.do?"
# url_kaisai = url_oddspark + "/KaisaiRaceList.do"

# url_oneday = url_oddspark + "/OneDayRaceList.do?"

class OneRace(Racers):

  def __init__(self, date: str, place: str, race_no: int):

    self.json_path = "../../ruby/gosu/gosu_race/test_new.json"

    self.race_no = race_no
    self.p_race = f"raceDy={date}&placeCd={self.placeCd_d[place]}&raceNo={str(race_no)}"
    self.p_pred = f"/{self.placeEn_d[place]}/{date[:4]}/{date[4:]}.html"
    self.p_predai = f"/ai/OneDayRaceList.do?raceDy={date}&placeCd={self.placeCd_d[place]}&aiId=1"
    
    self.entry_soup = self.get_soup(self.url_racelist + self.p_race)
    # self.pred_soup = self.get_soup(self.url_pred + self.p_pred)

    self.result_soup = self.get_soup(self.url_result + self.p_race)
    
    self.pred_soup = ""
    self.predai_soup = ""
    self.row_size = len(self.entry_soup.find_all("td", class_="showElm racer"))
    self.odds_d = { n : ("") for n in range(1, self.row_size + 1)}
    self.pred_d = { n : ("", "", "") for n in range(1, self.row_size + 1)}
    self.predai_d = { n : ("", "", "") for n in range(1, self.row_size + 1)}
    self.sohyo = ""

    self.racetitle = self.raceTitle()
    # print(self.racetitle)

  def sr_racer_latest(self) -> pd.Series:
    name = "Latest"
    lst = ["no", "選手名", "q10/90", "t10/90", "dry/wet", "LG"]
    lst += ["次走", "前走", "前々走", "3走前", "4走前", "5走前"]
    sr = pd.Series([np.nan] * len(lst), index=lst, name=name, dtype=object)

    return sr

  def raceTitle(self):
    # 一般戦 2021年6月25日(金) 伊勢崎 3R 15:21
    soup = self.entry_soup
    shubetsu, race = "OddsPark AutoRace", ""
    res = soup.find("title")
    if res and res.text != "オッズパークオートレース":
        shubetsu, race = res.text.split("｜")[:2] # race: 日程 場所 レース
        shubetsu = shubetsu.strip('【レース別出走表】') # 種別
    stm = soup.select_one(".RCstm")
    stm_txt = "spam ??:??" if not stm else stm.text
    start_time = stm_txt.split()[1] # 発走時刻
    dst = soup.select_one(".RCdst")
    dst_txt = "天候：?? 走路状況：?? spam" if not dst else dst.text
    weather, surface = dst_txt.split()[:2]
    surface = "(" + surface.strip("走路状況：") + ")"
    title = " ".join([shubetsu, race, start_time, weather, surface])
    return title
      
  def entry_raps(self):

    df = self.get_dfs(self.entry_soup)[0]
    if df.empty: 
        return df
    sr_lst = []
    for n in range(len(df)):
      sr = self.sr_racer()
      racer_l = df.values[n][:7]
      racer = [re.sub("  |\u3000", " ", r) for r in racer_l if type(r) == str]
      # print(racer)
      # -> ['城戸 徹 41歳/27期 V0/0回/V1 ヤブキ３７３/1', '飯 塚', 
      # -> '0m 3.89 0.073', 'B-43 (B-46) 53.433', '3.39 3.463 3.423', '着順：0-0-0-7 0.16 ..']
      fstname, lstname, age, v, machine = racer[0].split()
      name = fstname + " " + lstname
      lg = racer[1].replace(" ", "")
      racer2s = racer[2].split()
      if "再" in racer2s: racer2s.remove("再") 
      handicap, tryLap, tryDev = racer2s # ハンデ、試走タイム、試走偏差
      rank, prvRank, point = racer[3].split() # ランク、(前ランク)、審査ポイント
      avgTry, avgLap, fstLap = racer[4].split() # 良10走lap
      # print(tryLap)
      last10, ast = racer[5].split()[:2] # 近10走着順、平均ST
      sr["no"] = str(n + 1)
      sr["name"] = name
      sr["age"] = re.sub("/", "-", age)
      sr["lg"] = lg
      sr["rank"] = rank
      sr["prank"] = prvRank
      sr["hand"] = handicap
      sr["machine"] = re.sub("/1", "", machine)
      sr["vc"] = re.sub("/", "-", v)
      sr["point"] = float(point)
      sr["last"] = last10.strip("着順：")
      sr['ast'] = ast
      if self.is_num(tryLap):
        sr["try"] = float(tryLap)
        sr["prd"] = round(float(tryLap) + float(tryDev), 3)
      sr["avt"] = float(avgTry)
      sr["avg"] = float(avgLap)
      sr["fst"] = float(fstLap)
      sr.name = n
      sr_lst.append(sr)

    hands = [sr["hand"] for sr in sr_lst]
    # avtLaps = [sr["avt"] for sr in sr_lst] 
    avgLaps = [sr["avg"] for sr in sr_lst]
    fstLaps = [sr["fst"] for sr in sr_lst]
    prdLaps = [sr["prd"] for sr in sr_lst]
    # avtDifs = self.calc_goalDifs(avtLaps, hands)
    avgDifs = self.calc_goalDifs(avgLaps, hands)
    fstDifs = self.calc_goalDifs(fstLaps, hands)
    prdDifs = self.calc_goalDifs(prdLaps, hands)
    for sr, avgDif, fstDif, prdDif in zip(sr_lst, avgDifs, fstDifs, prdDifs):
        # sr["atm"] = avtDif
        sr["avm"] = round(avgDif, 1)
        sr["fsm"] = round(fstDif, 1)
        sr["pdm"] = round(prdDif, 1)
    
    raps_df = pd.DataFrame(sr_lst).dropna(how="all", axis=1)
    
    return raps_df

  def entry_latests(self) -> pd.DataFrame:

    title = self.racetitle
    date_str = title.split()[1][:-3]
    date_dt = datetime.datetime.strptime(date_str, "%Y年%m月%d日")
    dt = str(date_dt.month) + "/" + str(date_dt.day)
    rc = "".join(title.split()[2:4])
    thisrace = " ".join([dt, rc])
    thiscond = title.split()[6][1]

    df = self.get_dfs(self.entry_soup)[0]
    names = [df.iloc[n, :2] for n in range(len(df))]
    lgs = ["".join(df.iloc[n, 2].split()) for n in range(len(df))]
    rates = [df.iloc[n, 6] for n in range(len(df))]
    drywet = [df.iloc[n, 7] for n in range(len(df))]
    handis = [df.iloc[n, 3].split()[0] for n in range(len(df))]
    latest = [df.iloc[n, 8:] for n in range(len(df))]
    srs = []
    for i in range(len(df)*2):
      sr = self.sr_racer_latest()
      j = i // 2
      if not i & 1:
        sr.name = i
        sr["no"] = names[j][0]
        sr["選手名"] = " ".join(names[j][1].split()[:2])
        sr["q10/90"] = rates[j].split()[3].strip("：")
        sr["t10/90"] = rates[j].split()[5].strip("：")
        sr["dry/wet"] = drywet[j].split()[1].strip("良：")
        sr["LG"] = lgs[j]
        lst5 = latest[j]["前5走成績"]
        sr["次走"] = thisrace
        sr["前走"] = " ".join(lst5["前走"].split()[:2])
        sr["前々走"] = " ".join(lst5["前々走"].split()[:2])
        sr["3走前"] = " ".join(lst5["3走前"].split()[:2])
        sr["4走前"] = " ".join(lst5["4走前"].split()[:2])
        sr["5走前"] = " ".join(lst5["5走前"].split()[:2])
        srs.append(sr)
      else:
        sr.name = i
        sr["no"] = " "
        sr["選手名"] = " "
        sr["q10/90"] = rates[j].split()[9].strip("：")
        sr["t10/90"] = rates[j].split()[11].strip("：")
        sr["dry/wet"] = drywet[j].split()[3].strip("湿：")
        sr["LG"] = " "
        lst5 = latest[j]["前5走成績"]
        sr["次走"] = thiscond + " " + handis[j] + " ?着"
        sr["前走"] = " ".join(lst5["前走"].split()[2:5])
        sr["前々走"] = " ".join(lst5["前々走"].split()[2:5])
        sr["3走前"] = " ".join(lst5["3走前"].split()[2:5])
        sr["4走前"] = " ".join(lst5["4走前"].split()[2:5])
        sr["5走前"] = " ".join(lst5["5走前"].split()[2:5])
        srs.append(sr)
    
    e_df = pd.DataFrame(srs)
    p_df = self.predction_for_concat()

    return pd.concat([e_df, p_df], axis=1)

  def dspEntry(self):
    df = self.entry().dropna(how="all", axis=1)
    cm = sns.light_palette("green", as_cmap=True)
    # print(self.racetitle)
    # display(df.style.background_gradient(cmap=cm))
    print(df)

  def result(self):

    df = self.get_dfs(self.result_soup)[0]
    if df.empty: 
      return df
    s_df = df.sort_values('車')
    sr_odr, sr_fav = s_df["着"], s_df["人気"]
    odrs = [str(int(odr)) if self.is_num(odr) else odr for odr in sr_odr]
    favs = [str(int(fav)) if self.is_num(fav) else fav for fav in sr_fav]
    laps = list(s_df["競走タイム"])
    hands = list(s_df["ハンデ"])
    goalDiffs = self.calc_goalDifs(laps, hands)

    result_df = self.entry()
    for n in range(len(result_df)): 
      result_df.loc[n, "run"] = laps[n]
      result_df.loc[n, "rnm"] = goalDiffs[n]
      result_df.loc[n, "odr"] = odrs[n]
      result_df.loc[n, "fav"] = favs[n]
    
    return result_df
      
  def dspResult(self):
    df = self.result()
    cm = sns.light_palette("green", as_cmap=True)
    print(self.racetitle)
    # display(df.style.background_gradient(cmap=cm).hide_index())

  def saveDf2json(self, df: pd.DataFrame):
    if df.empty:
      print("a dataframe is empty.")
      return
    j = df.to_json(force_ascii=False)
    dic = json.loads(j)
    title = self.racetitle
    dic["title"] = title
    j_with_title = json.dumps(dic, ensure_ascii=False)
    # p = "../../ruby/gosu/gosu_race/test_new.json"
    p = self.json_path
    with open(p, "w", encoding="utf-8") as f:
      f.write(j_with_title)
    print(f"saved dataframe: '{title}' to json")

  def savEntry(self):
    df = self.entry()
    self.saveDf2json(df)

  def savResult(self):
    df = self.result()
    self.saveDf2json(df)

  def reqPrediction(self):
    soup = self.get_soup(self.url_pred + self.p_pred)
    lst = soup.find_all("p", class_="sohyo")
    sohyo = "総評:" + lst[self.race_no - 1].find("strong").text.strip("（総評）")
    dfs = self.get_dfs(soup)
    _df = dfs[self.race_no - 1].dropna(thresh=9)
    pred_df = _df.fillna("")
    lst = []
    for e in pred_df.itertuples():
      lst.append([e.晴, e.スタート, e.コメント])
        
    return pd.DataFrame(lst, columns=["晴", "ST", "Commnet"]) #, sohyo

  def predction_for_concat(self):
    ai_df = self.reqPredicionAI()
    p_df = self.reqPrediction()
    lst = []
    for ai, p in zip(ai_df.itertuples(), p_df.itertuples()):
        lst.append(ai[1:] + p[1:])
        lst.append((" ", " ", " ", " ", " ", " "))
    cols = list(ai_df.columns) + list(p_df.columns)
    
    return pd.DataFrame(lst, columns=cols)
    
  def reqPredicionAI(self):
    soup = self.get_soup(self.url_pred + self.p_predai)
    dfs = self.get_dfs(soup)
    df = dfs[self.race_no - 1]
    lst = []
    for i in range(len(df)):
      steady = df.iloc[i, 4:7]["AI予想印"][0]
      oneshot = df.iloc[i, 4:7]["AI予想印"][1]
      justbe4 = df.iloc[i, 4:7]["AI予想印"][2]
      lst.append((steady, oneshot, justbe4))
    
    return pd.DataFrame(lst, columns=["堅実", "一発", "直前"])



if __name__=='__main__':

  race = OneRace('20210817','飯塚', 10)
  print(race.racetitle)
  # df = race.reqPrediction()
  # df = race.entry_latests()
  # print(df)
  df = race.predction_for_concat()
  # race.savResult()
  print(df)
    
  # sr = race.srPayout()
  # print(sr)
  # race.bet([1, 2, 3])
  # race.balance()
  