import tkinter as tk
from tkinter import ttk
import pandas as pd
import unicodedata
import seaborn as sns
from onerace import OneRace
from odds import RaceOdds
from result import Result

class TkResult:
  
  def __init__(self, title: str, dfs: list):
    self.root = tk.Toplevel()
    # self.root = tk.Tk()
    self.root.title(title)
    self.frame = tk.Frame(self.root)
    self.rlt_df = dfs[0]
    self.note_df = dfs[1]
    self.pay1_df = dfs[2]
    self.pay2_df = dfs[3]

    sizes = self.column_sizes(self.rlt_df)
    w = sum(map(lambda x: x+8, sizes)) + 30
    h = 650
    self.root.geometry(f"{w}x{h}+300+350")
    self.title = title

  def set_table(self, df: pd.DataFrame, side: object):
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
    f_table.pack(side=side, anchor=tk.NW)

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
    self.set_table(self.rlt_df, tk.TOP)
    self.set_table(self.note_df, tk.TOP)
    self.set_table(self.pay1_df, tk.LEFT)
    self.set_table(self.pay2_df, tk.LEFT)
    self.frame.pack()
    self.root.mainloop()

if __name__ == '__main__':

  # iris = sns.load_dataset('iris')
  # df = iris.head(6)
  # dfs = [df]
  r = Result('20210818','飯塚', 3)
  title = r.raceTitle()
  rslt = r.result()
  note = r.groundnote()
  pay = r.payout()
  dfs = [rslt, note, *pay]
  t = TkResult(title, dfs)
  t.run()