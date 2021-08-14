import tkinter as tk
from tkinter import ttk
import pandas as pd
import unicodedata
from race import Race
import seaborn as sns

class TkRaces:
  
  def __init__(self, date_place: str, titles: list, dfs: list):
    self.root = tk.Tk()
    self.root.title(date_place)
    self.titles = titles
    self.dfs = dfs

    self.root.geometry("600x900")
    self.canvas = tk.Canvas(self.root)
    # Canvasのスクロールバー
    bar = tk.Scrollbar(self.canvas, orient=tk.VERTICAL)
    bar.pack(side=tk.RIGHT, fill=tk.Y)
    bar.config(command=self.canvas.yview)
    self.canvas.config(yscrollcommand=bar.set)
    # Canvasのスクロール範囲を設定
    self.canvas.config(scrollregion=(0, 0, 0, 910*3))
    self.canvas.pack(fill=tk.BOTH, expand=True) # tk.BOTH：縦横両方向に対して引き伸ばす

  def races(self, dfs: list):
    
    # Frame = tk.Frame(self.canvas, bg="whitesmoke", padx=10, pady=5)
    Frame = tk.Frame(self.canvas)
    # for df in dfs[0]:
    for r in [0, 2, 4, 6, 8, 10, 12]:
      self.race(Frame, dfs[0], r)
    Frame.pack()
    self.canvas.create_window((0,0), window=Frame, anchor=tk.NW)

  def race(self, frame, df: pd.DataFrame, r):

    # f_top.pack(fill=tk.X)

    l_title = tk.Label(frame, text="this is title.", bg="whitesmoke", anchor="w")
    # l_title.pack(side=tk.LEFT, expand=True, anchor=tk.W)
    l_title.grid(row=r, column=0, sticky=tk.W, pady=10, padx=10)

    b_quit = ttk.Button(frame, text='Quit', command=lambda: self.root.quit())
    # b_quit.pack(side=tk.LEFT, expand=True, anchor=tk.E)
    b_quit.grid(row=r, column=1, sticky=tk.E, pady=10, padx=10)

    headingcolor = "lightgrey"
    alternatecolor = "whitesmoke"

    tree = ttk.Treeview(frame, height=len(df)+1)

    def fixed_map(option):
      # Fix for setting text colour for Tkinter 8.6.9
      # From: https://core.tcl.tk/tk/info/509cafafae
      #
      # Returns the style map for 'option' with any styles starting with
      # ('!disabled', '!selected', ...) filtered out.
      #
      # style.map() returns an empty list for missing options, so this
      # should be future-safe.
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
      tree.column(i, width=size+8) # 
    
    lst = [tuple(t)[1:] for t in df.itertuples()]
    for i, tpl in enumerate(lst):
      tree.insert("", "end", tags=i, values=tpl)
      if i & 1:
        tree.tag_configure(i, background=alternatecolor)
    
    # tree.pack(side=tk.BOTTOM, anchor=tk.S)
    tree.grid(row=r+1, column=0, columnspan=2, pady=10, padx=10)

  def column_sizes(self, df: pd.DataFrame) -> list:

    def ea_width_count(text):
      count = 0
      for c in text:
        if unicodedata.east_asian_width(c) in 'FWA':
          count += 2
        else:
          count += 1
      return count * 8
    
    lst_columns = [[col] + list(df[col]) for col in df.columns]
    col_sizes = []
    for cols in lst_columns:
      col_sizes.append(max([ea_width_count(str(e)) for e in cols]))

    return col_sizes

  def run(self):
    self.races(self.dfs)
    self.root.mainloop()


if __name__ == '__main__':

  date_place = "auto race"
  titles = ["test"]
  iris = sns.load_dataset('iris')
  df = iris.head(6)
  dfs = [df]
  # print(date_place)
  # print(len(titles))
  # print(len(dfs))
  t = TkRaces(date_place, titles, dfs)
  t.run()