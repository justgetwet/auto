import tkinter as tk
from tkinter import ttk
import pandas as pd
import unicodedata
import seaborn as sns
from onerace import OneRace
from odds import RaceOdds

class TkOdds:
  
  def __init__(self, title: str, dfs: list):
    self.root = tk.Toplevel()
    # self.root = tk.Tk()
    self.root.title(title)
    self.frame = tk.Frame(self.root)
    self.win_df = dfs[0]
    self.quin_df = dfs[1]
    self.exa_df = dfs[2]
    self.trio_df = dfs[3]
    self.trif_df = dfs[4]
    
    w = 0
    for df in dfs:
      sizes = self.column_sizes(df)
      w += sum(map(lambda x: x+8, sizes)) + 30
    h = 500
    self.root.geometry(f"{w}x{h}+200+50")
    self.title = title

  def set_table(self, df: pd.DataFrame):
    f_table = tk.Frame(self.frame, pady=5, padx=5)
    headingcolor = "lightgrey"
    alternatecolor = "whitesmoke"

    tree = ttk.Treeview(f_table, height=len(df)+1)

    def fixed_map(option):
      # Fix for setting text colour for Tkinter 8.6.9
      # From: https://core.tcl.tk/tk/info/509cafafae
      #
      # From: https://ja.stackoverflow.com/questions/64095/
      # Python ttk.Treeview python3.7でリストに割り当てたtagに対して色を設定する方法
      return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]	
    
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview.Heading", background=headingcolor)
    style.map('Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))
    
    tree["show"] = "headings"
    cols = tuple(range(1, len(df.columns)+1))
    tree['columns'] = cols

    sizes = self.column_sizes(df)
    for i, col, size in zip(cols, df.columns, sizes):
      tree.heading(i, text=f"{col}")
      tree.column(i, width=size+8)
    
    tpls = [tuple(t)[1:] for t in df.itertuples()]
    for i, tpl in enumerate(tpls):
      tree.insert("", "end", tags=i, values=tpl)
      if i & 1:
        tree.tag_configure(i, background=alternatecolor)
    
    tree.pack(pady=5, padx=5)
    f_table.pack(side=tk.LEFT, anchor=tk.NW)

  def column_sizes(self, df: pd.DataFrame) -> list:

    def east_asian_width_count(text):
      count = 0
      for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
          count += 2
        else:
          count += 1
      return count * 8
    
    lst_columns = [[col] + list(df[col]) for col in df.columns]
    sizes = []
    for cols in lst_columns:
      max_size = max([east_asian_width_count(str(col)) for col in cols])
      sizes.append(max_size)

    return sizes

  def run(self):
    self.set_table(self.win_df)
    self.set_table(self.quin_df)
    self.set_table(self.exa_df)
    self.set_table(self.trio_df)
    self.set_table(self.trif_df)
    self.frame.pack()
    self.root.mainloop()

if __name__ == '__main__':

  # iris = sns.load_dataset('iris')
  # df = iris.head(6)
  # dfs = [df]
  ro = RaceOdds('20210818','飯塚', 3)
  win = ro.reqWin()
  quin = ro.reqQuin()
  exa = ro.reqExa()
  trio = ro.reqTrio()
  trif = ro.reqTrif()
  dfs = [win, quin, exa, trio, trif]
  t = TkOdds("odds data", dfs)
  t.run()