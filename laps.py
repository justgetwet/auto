# import urllib.request
# from bs4 import BeautifulSoup
from onerace import OneRace
import json

class Laps(OneRace):

  def __init__(self, date: str, place: str, race_no: int):
    super().__init__(date, place, race_no)
    self.srs_handicap = self.entry_handicaps()

    p = "./racer_codes.json"
    with open(p, "r", encoding="utf-8") as f:
      read_dic = json.load(f)

    self.d_code = read_dic

  def test(self):
    return self.srs_handicap

  def get_laps(self, name, hand):

    detail_url = "https://www.oddspark.com/autorace/PlayerDetail.do?"
    cd = self.d_code[name]
    url = detail_url + "playerCd=" + cd
    soup = self.get_soup(url)
    dfs = self.get_dfs(soup)
    df = dfs[8]

    _laps = []
    for i, sr in df.iterrows():
      if sr["走路  (天候)"][0] == "良" and sr["H"] == hand.strip("m"):
        _laps.append(sr["競走T"])
    laps = [lap for lap in _laps if isinstance(lap, float) and lap != 0.0]
    
    return laps

  def select_latest_laps(self):
    avgGoaldifs = self.calc_goalDifs()
    topTime = self.calc_avgTopTime()
    tpls = []
    for sr, avgdif in zip(self.srs_handicap, avgGoaldifs):
      no = sr["no"]
      name = sr["name"]
      handi = sr["handicap"]
      avgLap = sr["avgLap"]
      laps = self.get_laps(name, handi)
      gdifs = self.calc_goalDifs_raps(topTime, handi, laps)
      tpls.append((no, name, handi, float(avgLap), avgdif, laps, gdifs))

    return tpls

  def calc_goalDifs(self, mps=0.034) -> list:

    avgLaps = [float(sr["avgLap"]) for sr in self.srs_handicap]
    handis = [sr["handicap"] for sr in self.srs_handicap]

    f_handis = [float(handi.strip("m")) for handi in handis]
    c1 = avgLaps.pop(0)
    avgLaps.insert(0, c1 + 0.01)
    goalTimes = [lap * (31.0 + f_hand/100) for lap, f_hand in zip(avgLaps, f_handis)]
    goals = [gt for gt in goalTimes if gt != 0.0] # 失格など
    topTime = min(goals)
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
  
  laps = Laps('20210817','飯塚', 9)
  print(laps.raceTitle())
  for tpl in laps.select_latest_laps():
    print(tpl[0], tpl[1], tpl[4], tpl[6])