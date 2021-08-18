from ssl import DefaultVerifyPaths
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

class Result(Racers):

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

  def result(self):

    df = self.get_dfs(self.result_soup)[0]
    if df.empty: 
      return df
    # s_df = df.sort_values('車')
    # sr_odr, sr_fav = s_df["着"], s_df["人気"]
    # odrs = [str(int(odr)) if self.is_num(odr) else odr for odr in sr_odr]
    # favs = [str(int(fav)) if self.is_num(fav) else fav for fav in sr_fav]
    # laps = list(s_df["競走タイム"])
    # hands = list(s_df["ハンデ"])
    # goalDiffs = self.calc_goalDifs(laps, hands)
    # result_df = self.entry()
    # for n in range(len(result_df)): 
    #   result_df.loc[n, "run"] = laps[n]
    #   result_df.loc[n, "rnm"] = goalDiffs[n]
    #   result_df.loc[n, "odr"] = odrs[n]
    #   result_df.loc[n, "fav"] = favs[n]
    
    return df.fillna("")

  def groundnote(self):
    return self.get_dfs(self.result_soup)[1]

  def payout(self):
    dfs = self.get_dfs(self.result_soup)[2:4]
    # if df.empty: 
    #   return df

    return dfs[0].fillna(""), dfs[1].fillna("")

  def srPayout(self):
    soup = self.result_soup
    dfs = self.get_dfs(soup)

    is_goal = dfs[1].iloc[0, 0] == "ゴール線通過"
    order_lst = list(dfs[0]["着"][:4])
    if type(order_lst[0]) == str:
      order_lst = [int(s) for s in order_lst if self.is_num(s)]
    is_order = order_lst == [1, 2, 3, 4]
    sr = pd.Series(0.0)
    if is_goal and is_order:
      race_title = soup.select_one("title").get_text().split("｜")[1]
      title = ["title", race_title]
      race_weather = soup.select_one("li.RCdst").get_text(strip=True).split()[0]
      race_weather = race_weather.strip("天候：")
      weather = ["wthr", race_weather]
      v1 = ["1st", dfs[0]["車"][0]]
      v2 = ["2nd", dfs[0]["車"][1]]
      v3 = ["3rd", dfs[0]["車"][2]]
      v4 = ["1stf", dfs[0]["人気"][0]]
      v5 = ["2ndf", dfs[0]["人気"][1]]
      v6 = ["3rdf", dfs[0]["人気"][2]]
      df2 = dfs[2].set_index(0)
      df3 = dfs[3].set_index(0)
      v7 = ["win", df2.at["単勝", 2]]
      v8 = ["quin", df2.at["2連複", 2]]
      v9 = ["exac", df2.at["2連単", 2]]
      v10 = ["trio", df3.at["3連複", 2]]
      v11 = ["trif", df3.at["3連単", 2]]
      values = [title, weather, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11]
      index, value = zip(*values)
      sr = pd.Series(value, index=index)

    return sr

if __name__ == '__main__':

  r = Result('20210817','飯塚', 10)
  print(r.racetitle)

  # df = r.result()
  # print(df)
  df1, df2 = r.payout()
  print(df1)
  print(df2)
  df = r.groundnote()
  print(df)