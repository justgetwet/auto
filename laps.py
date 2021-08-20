# import urllib.request
# from bs4 import BeautifulSoup
from onerace import OneRace
import json

class Laps(OneRace):

  def __init__(self, date: str, place: str, race_no: int):
    super().__init__(date, place, race_no)
    self.detail_url = "https://www.oddspark.com/autorace/PlayerDetail.do?"
    self.srs_handicap = self.entry_handicaps()

    p = "./racer_codes.json"
    with open(p, "r", encoding="utf-8") as f:
      read_dic = json.load(f)

    self.d_code = read_dic

  def test(self):
    return self.srs_handicap

  def get_laps(self, name, handi):

    cd = self.d_code[name]
    url = self.detail_url + "playerCd=" + cd
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = dfs[8]

    eqh_laps, lst_laps, try_laps = [], [], []
    for i, sr in df.iterrows():
      if sr["走路  (天候)"][0] == "良" and i < 10:
        lst_laps.append(sr["競走T"])
        try_laps.append(sr["試走T"])
      if sr["走路  (天候)"][0] == "良" and sr["H"] == handi.strip("m"):
        eqh_laps.append(sr["競走T"])

    last10_laps = [lap for lap in lst_laps if isinstance(lap, float) and lap != 0.0]
    eqhandi_laps = [lap for lap in eqh_laps if isinstance(lap, float) and lap != 0.0]
    try10_laps = [lap for lap in try_laps if isinstance(lap, float) and lap != 0.0]

    return last10_laps, eqhandi_laps, try10_laps

  def select_latest_laps(self):

    avgLaps = [float(sr["avgLap"]) for sr in self.srs_handicap]
    # print(avgLaps, tryLaps, prdLaps)
    avgDifs = self.calc_goalDifs(avgLaps)
    topTime = self.calc_avgTopTime()
    tpls = []
    for sr, avgdif in zip(self.srs_handicap, avgDifs):
      no = sr["no"]
      name = sr["name"]
      handi = sr["handicap"]
      avgLap = sr["avgLap"]
      tryLap = sr["tryLap"]
      prdLap = sr["prdLap"]
      lst_laps, eqh_laps, try_laps = self.get_laps(name, handi)
      lst_difs = self.calc_goalDifs_raps(topTime, handi, lst_laps)
      eqh_difs = self.calc_goalDifs_raps(topTime, handi, eqh_laps)
      try_difs = self.calc_goalDifs_raps(topTime, handi, try_laps)
      try_dif = self.calc_goalDifs_raps(topTime, handi, [float(tryLap)])[0]
      prd_dif = self.calc_goalDifs_raps(topTime, handi, [float(prdLap)])[0]
      tp = (no, name, handi, float(avgLap), avgdif, lst_difs, eqh_difs, try_difs, try_dif, prd_dif)
      tpls.append(tp)

    return tpls

  def calc_goalDifs(self, laps: list, mps=0.034) -> list:

    # avgLaps = [float(sr["avgLap"]) for sr in self.srs_handicap]
    handis = [sr["handicap"] for sr in self.srs_handicap]

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

    # avgLaps = [float(sr["avgLap"]) for sr in self.srs_handicap]
    handis = [sr["handicap"] for sr in self.srs_handicap]

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

    avgLaps = [float(sr["avgLap"]) for sr in self.srs_handicap]
    handis = [sr["handicap"] for sr in self.srs_handicap]

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
  for tpl in laps.select_latest_laps():
    print(tpl)
    # print(tpl[0], tpl[1], tpl[4], tpl[6])