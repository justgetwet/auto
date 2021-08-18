import numpy as np
import pandas as pd
import re
import json
import copy
import seaborn as sns
from racers import Racers
# pd.set_option('display.max_columns', 22)
# from race import Scrape, RaceUrls
from racers import Racers

class RaceOdds(Racers):

  def __init__(self, date: str, place: str, race_no: int):

    self.json_path = "../../ruby/gosu/gosu_race/test_new.json"

    self.race_no = race_no
    self.p_race = f"raceDy={date}&placeCd={self.placeCd_d[place]}&raceNo={str(race_no)}"
    self.p_pred = f"/{self.placeEn_d[place]}/{date[:4]}/{date[4:]}.html"
    self.p_predai = f"/ai/OneDayRaceList.do?raceDy={date}&placeCd={self.placeCd_d[place]}&aiId=1"
    
    self.entry_soup = self.get_soup(self.url_racelist + self.p_race)
    self.result_soup = self.get_soup(self.url_result + self.p_race)
    
    self.pred_soup = ""
    self.predai_soup = ""
    self.row_size = len(self.entry_soup.find_all("td", class_="showElm racer"))
    self.odds_d = { n : ("") for n in range(1, self.row_size + 1)}
    self.pred_d = { n : ("", "", "") for n in range(1, self.row_size + 1)}
    self.predai_d = { n : ("", "", "") for n in range(1, self.row_size + 1)}
    self.sohyo = ""

    self.racetitle = self.raceTitle()

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
      
  def reqWin(self):
    opt = "&betType=1&viewType=0"
    url = self.url_odds + self.p_race + opt
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = pd.DataFrame()
    if not dfs[0].empty:
      _df = self.get_dfs(soup)[0]
      cols = [4, 5, 6, 7, 8]
      df = _df.drop(_df.columns[cols], axis=1).fillna("")
      df.columns = ["車番", "選手名", "単勝", "複勝"]
    
    return df

  def reqQuin(self):
    opt = "&betType=6&viewType=0"
    url = self.url_odds + self.p_race + opt
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = pd.DataFrame()
    if not dfs[0].empty and len(dfs) > 2:
      df = dfs[2]
      cols = [c for i, c in enumerate(df.columns) if not i == 0 and not i & 1]
      for i in range(len(cols)):
        ls = [e if pd.isna(e) else "[" + str(int(e)) + "]" for e in df[cols[i]]]
        sr = pd.Series(ls, dtype=object)
        df[cols[i]] = sr
      
      sr = pd.Series(["[" + str(e) + "]" for e in df["1"]])
      df["1"] = sr
      new_cols = ["[" + re.sub(".1", "]", c) if c[1:] == ".1" else c for c in df.columns]
      df.columns = new_cols

    return df.fillna("")

  def reqExa(self):
    opt = "&betType=5&viewType=1"
    url = self.url_odds + self.p_race + opt
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = pd.DataFrame()
    if not dfs[0].empty and len(dfs) > 2:
      df = dfs[2]

    return df

  def reqTrio(self):
    opt = "&betType=9&viewType=1"
    url = self.url_odds + self.p_race + opt
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = pd.DataFrame()
    if not dfs[0].empty and len(dfs) > 2:
      df = dfs[2]

    return df

  def reqTrif(self):
    opt = "&betType=8&viewType=1"
    url = self.url_odds + self.p_race + opt
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = pd.DataFrame()
    if not dfs[0].empty and len(dfs) > 2:
      df = dfs[2]

    return df

if __name__ == '__main__':
  
  race = RaceOdds('20210818','飯塚', 6)
  # df = race.reqWin()
  # print(df)
  # df = race.reqQuin()
  # df = race.reqExa()
  df = race.reqTrif()
  print(df)