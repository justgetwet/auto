import tkinter as tk
from tkinter import ttk
import pandas as pd
import unicodedata
# import seaborn as sns
from onerace import OneRace

class TkRace:
  
  def __init__(self, title: str, dfs: list):
    self.root = tk.Toplevel()
    # self.root = tk.Tk()
    self.root.title("Auto Race")
    self.rap_df = dfs[0]
    self.lst_df = dfs[1]
    sizes = self.column_sizes(self.lst_df)
    w = sum(map(lambda x: x+8, sizes)) + 60
    h = 800
    self.root.geometry(f"{w}x{h}+200+50")
    self.title = title
    self.frame = tk.Frame(self.root)

  def set_toolbar_frame(self):
    f_toolbar = tk.Frame(self.frame, height=50, pady=10, padx=10)
    f_toolbar.pack(fill=tk.X)
    
    l_title = tk.Label(f_toolbar, text=self.title, anchor="w")
    l_title.pack(side=tk.LEFT, expand=True, anchor=tk.W)

    b_quit = ttk.Button(f_toolbar, text='Quit', command=lambda: self.root.quit())
    b_quit.pack(side=tk.LEFT, expand=True, anchor=tk.E)

  def set_raps_on_frame(self):
    f_raps = tk.Frame(self.frame, pady=10, padx=10)
    df = self.rap_df
    headingcolor = "lightgrey"
    alternatecolor = "whitesmoke"

    tree = ttk.Treeview(f_raps, height=len(df)+1)

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
    
    tree.pack(pady=10, padx=10)
    # f_raps.pack(fill=tk.BOTH, anchor=tk.W)
    f_raps.pack(side="top", expand=0, anchor=tk.W)

  def set_latest_on_frame(self):
    f_latest = tk.Frame(self.frame, pady=10, padx=10)
    df = self.lst_df
    headingcolor = "lightgrey"
    alternatecolor = "whitesmoke"

    tree = ttk.Treeview(f_latest, height=len(df)+1)

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
    
    tree.pack(pady=10, padx=10)
    f_latest.pack(fill=tk.BOTH)

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
    self.set_toolbar_frame()
    self.set_raps_on_frame()
    self.set_latest_on_frame()
    self.frame.pack()
    self.root.mainloop()

if __name__ == '__main__':
  
  race = OneRace('20210816','飯塚', 3)
  title = race.racetitle
  r_df = race.entry_raps()
  l_df = race.entry_latests()
  t = TkRace(title, [r_df, l_df])
  t.run()