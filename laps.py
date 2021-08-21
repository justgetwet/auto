# import urllib.request
# from bs4 import BeautifulSoup
import pandas as pd
from onerace import OneRace
from result import Result
import json

class Laps(OneRace):

  def __init__(self, date: str, place: str, race_no: int):
    super().__init__(date, place, race_no)
    self.detail_url = "https://www.oddspark.com/autorace/PlayerDetail.do?"
    self.srs_entrydata = self.entry_data()
    self.title = self.raceTitle()

    rlt = Result(date, place, race_no)
    self.result_df = rlt.result()

    p = "./racer_codes.json"
    with open(p, "r", encoding="utf-8") as f:
      read_dic = json.load(f)

    self.d_code = read_dic

  def get_laps(self, name, handi):

    cd = self.d_code[name]
    url = self.detail_url + "playerCd=" + cd
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = dfs[8]

    lstLaps, tryLaps, lstSTs, eqhLaps = [], [], [], []
    for i, sr in df.iterrows():
      if sr["走路  (天候)"][0] == "良" and i < 10:
        lstLaps.append(sr["競走T"])
        tryLaps.append(sr["試走T"])
        lstSTs.append(sr["ST"])
      if sr["走路  (天候)"][0] == "良" and sr["H"] == handi.strip("m"):
        eqhLaps.append(sr["競走T"])
    lstLaps = [lap for lap in lstLaps if isinstance(lap, float) and lap != 0.0]
    eqhLaps = [lap for lap in eqhLaps if isinstance(lap, float) and lap != 0.0]
    tryLaps = [lap for lap in tryLaps if isinstance(lap, float) and lap != 0.0]
    lstSTs = [st for st in lstSTs if isinstance(st, float) and st != 0.0]

    return lstLaps, eqhLaps, tryLaps, lstSTs

  def test(self):
    if not self.result_df.empty:
      print(self.result_df)

  def pickup_and_calc(self):

    avgLaps = [float(sr["avgLap"]) for sr in self.srs_entrydata]
    avgDifs = self.calc_goalDifs(avgLaps)
    topTime = self.calc_avgTopTime()
    ranLaps = [0.0 for _ in range(len(avgDifs))]
    if not self.result_df.empty:
      runLaps = list(self.result_df["競走タイム"])
    stsec = 5
    srs = []
    for sr, avgDif, s_runLap in zip(self.srs_entrydata, avgDifs, runLaps):
      no = sr["no"]
      name = sr["name"]
      handi = sr["handicap"]
      avgLap = sr["avgLap"]
      tryLap, prdLap, runLap = 0.0, 0.0, 0.0
      if self.is_num(sr["tryLap"]):
        tryLap = float(sr["tryLap"])
        prdLap = float(sr["prdLap"])
      if self.is_num(s_runLap):
        runLap = float(s_runLap)
      lstLaps, eqhLaps, tryLaps, lstSTs = self.get_laps(name, handi)
      lstDifs = self.calc_goalDifs_raps(topTime, handi, lstLaps)
      eqhDifs = self.calc_goalDifs_raps(topTime, handi, eqhLaps)
      tryDifs = self.calc_goalDifs_raps(topTime, handi, tryLaps)
      tryDif = self.calc_goalDifs_raps(topTime, handi, [tryLap])[0]
      prdDif = self.calc_goalDifs_raps(topTime, handi, [prdLap])[0]
      runDif = self.calc_goalDifs_raps(topTime, handi, [runLap])[0]
      h = int(handi.strip("m"))
      stDifs = [(((stsec - st) / float(avgLap)) * 100) - h for st in lstSTs]
      idx = ["no", "name", "handi", "avgDif", "tryDif", "prdDif", "runDif"]
      idx += ["lstDifs", "eqhDifs", "tryDifs", "StDifs"]
      dat = [no, name, handi, avgDif, tryDif, prdDif, runDif, lstDifs, eqhDifs, tryDifs, stDifs]
      srs.append(pd.Series(dat, index=idx, name=self.title))

    return srs

  def calc_goalDifs(self, laps: list, mps=0.034) -> list:

    # avgLaps = [float(sr["avgLap"]) for sr in self.srs_entrydata]
    handis = [sr["handicap"] for sr in self.srs_entrydata]

    f_handis = [float(handi.strip("m")) for handi in handis]
    c1 = laps.pop(0)
    laps.insert(0, c1 + 0.01)
    goalTimes = [lap * (31.0 + f_hand/100) for lap, f_hand in zip(laps, f_handis)]
    goals = [gt for gt in goalTimes if gt != 0.0] # 失格など
    topTime = min(goals)
    _goalDiffs = [(topTime - gt) / mps if gt != 0.0 else "-" for gt in goalTimes]
    goalDiffs = [round(gds, 1) for gds in _goalDiffs]

    return goalDiffs

  def calc_goalDifs_toptime(self, topTime: float, laps: list, mps=0.034) -> list:

    # avgLaps = [float(sr["avgLap"]) for sr in self.srs_entrydata]
    handis = [sr["handicap"] for sr in self.srs_entrydata]

    f_handis = [float(handi.strip("m")) for handi in handis]
    c1 = laps.pop(0)
    laps.insert(0, c1 + 0.01)
    goalTimes = [lap * (31.0 + f_hand/100) for lap, f_hand in zip(laps, f_handis)]
    # goals = [gt for gt in goalTimes if gt != 0.0] # 失格など
    # topTime = min(goals)
    _goalDiffs = [(topTime - gt) / mps if gt != 0.0 else "-" for gt in goalTimes]
    goalDiffs = [round(gds, 1) for gds in _goalDiffs]

    return goalDiffs
  

  def calc_avgTopTime(self):

    avgLaps = [float(sr["avgLap"]) for sr in self.srs_entrydata]
    handis = [sr["handicap"] for sr in self.srs_entrydata]

    f_handis = [float(handi.strip("m")) for handi in handis]
    c1 = avgLaps.pop(0)
    avgLaps.insert(0, c1 + 0.01)
    goalTimes = [lap * (31.0 + f_hand/100) for lap, f_hand in zip(avgLaps, f_handis)]
    goals = [gt for gt in goalTimes if gt != 0.0] # 失格など
    topTime = min(goals)

    return topTime

  def calc_goalDifs_raps(self, topTime: float, handi: str, laps: list, mps=0.034):
    
    f_handi = float(handi.strip("m"))
    goalTimes = [lap * (31.0 + f_handi/100) for lap in laps]
    _goalDiffs = [(topTime - gt) / mps if gt != 0.0 else "-" for gt in goalTimes]
    goalDiffs = [round(gds, 1) for gds in _goalDiffs]

    return goalDiffs


if __name__ == '__main__':
  
  laps = Laps('20210820','浜松', 10)
  print(laps.raceTitle())
  print(laps.test())
  # for tpl in laps.pickup_and_calc():
  #   print(tpl)
    # print(tpl[0], tpl[1], tpl[4], tpl[6])