import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import unicodedata
import seaborn as sns
from onerace import OneRace
from odds import RaceOdds
from tkodds import TkOdds

class TkRace:
  
  def __init__(self, title: str, dfs: list, tpl: tuple):
    self.root = tk.Toplevel()
    # self.root = tk.Tk()
    self.tpl = tpl
    self.images = []
    self.root.title(title)
    self.dfs = [pd.DataFrame(), pd.DataFrame()]
    if len(dfs) == 2:
      self.dfs = dfs
    self.rap_df = self.dfs[0]
    self.lst_df = self.dfs[1]
    sizes = self.column_sizes(self.lst_df)
    w = sum(map(lambda x: x+8, sizes)) + 60
    h = 800
    self.root.geometry(f"{w}x{h}+100+50")
    self.title = title
    self.frame = tk.Frame(self.root)

  def set_topbar_frame(self):
    f_topbar = tk.Frame(self.frame, height=50, pady=0, padx=5)
    f_topbar.pack(fill=tk.X)
    
    self.set_images(f_topbar)

    b_quit = ttk.Button(f_topbar, text='Odds', command=lambda: self.show_odds())
    b_quit.pack(side=tk.LEFT, expand=True, anchor=tk.E)

  def set_images(self, frame):
    f_images = tk.Frame(frame, pady=5, padx=5)
    ranks = self.rap_df["rank"]
    names = self.rap_df["name"]
    colors = ["white", "black", "red", "blue", "yellow", "green", "orange"]
    colors = colors[:len(ranks)]
    for r, n, c in zip(ranks, names, colors):
      canvas = tk.Canvas(f_images, height=63, width=58, bg=c)
      canvas.pack(side=tk.LEFT)
      im_p = "./images/" + r + "_" + "".join(n.split()) + ".png"
      im = Image.open(im_p)
      # im.size -> 60 x 60
      img = ImageTk.PhotoImage(im)
      self.images.append(img)
      canvas.create_image(0, 0, image=img, anchor=tk.NW)

    f_images.pack(side=tk.LEFT, anchor=tk.W)

  def set_table(self, df: pd.DataFrame):
    f_table = tk.Frame(self.frame, pady=0, padx=5)
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
    # f_raps.pack(fill=tk.BOTH, anchor=tk.W)
    f_table.pack(side="top", expand=0, anchor=tk.W)

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

  def show_odds(self):
    ro = RaceOdds(*self.tpl)
    win = ro.reqWin()
    quin = ro.reqQuin()
    exa = ro.reqExa()
    trio = ro.reqTrio()
    trif = ro.reqTrif()
    dfs = [win, quin, exa, trio, trif]
    t = TkOdds(self.title, dfs, self.tpl)
    t.run()

  def run(self):
    self.set_topbar_frame()
    self.set_table(self.rap_df)
    self.set_table(self.lst_df)
    self.frame.pack()
    self.root.mainloop()

if __name__ == '__main__':
  
  tpl = ('20210816','飯塚', 3)
  race = OneRace(*tpl)
  title = race.racetitle
  raps = race.entry_raps()
  latests = race.entry_latests()
  dfs = [raps, latests]
  t = TkRace(title, dfs, tpl)
  t.run()