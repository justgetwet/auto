import tkinter as tk
from tkinter import ttk
import pandas as pd
from race import Race
from tksample import Scrollbar_Example

class TkRaces:

  def __init__(self, date_place: str, titles: list, dfs: list):
    self.root = tk.Tk()
    self.root.title(date_place)
    self.titles = titles
    self.dfs = dfs

    self.root.geometry("600x900")
    canvas = tk.Canvas(self.root)

    bar = tk.Scrollbar(canvas, orient=tk.VERTICAL)
    bar.pack(side=tk.RIGHT, fill=tk.Y)
    bar.config(command=canvas.yview)
    canvas.config(yscrollcommand=bar.set)
    # Canvasのスクロール範囲を設定
    canvas.config(scrollregion=(0, 0, 0, 910*3))
    canvas.pack(fill=tk.BOTH, expand=True) # tk.BOTH：縦横両方向に対して引き伸ばす
    # Canvasの上にFrameを載せる
    self.Frame = tk.Frame(canvas, bd=5)
    canvas.create_window((0,0), window=self.Frame, anchor=tk.NW)

  def child_window(self, event):
    app = Scrollbar_Example()


  def treev(self, title, df):

    lst = [tuple(t)[1:] for t in df.itertuples()]

    tree = ttk.Treeview(self.Frame, height=8)
    tree["show"] = "headings"
    tree['columns'] = (1, 2, 3, 4, 5, 6, 7, 8)
    tree.heading(1, text="No", anchor=tk.W)
    tree.heading(2, text="Name")
    tree.heading(3,text="LG")
    tree.heading(4, text="Handi")
    tree.heading(5, text="rank")
    tree.heading(6, text="point")
    tree.heading(7, text="trial")
    tree.heading(8, text="tridev")

    tree.column(1, width=30)
    tree.column(2, width=100)
    tree.column(3, width=60)
    tree.column(4, width=60)
    tree.column(5, width=60)
    tree.column(6, width=60)
    tree.column(7, width=60)
    tree.column(8, width=60)

    for i, tpl in enumerate(lst):
      tree.insert("", "end", tags=i, values=tpl)
      # if i & 1:
      #   tree.tag_configure(i, background="#CCFFFF")

    label = ttk.Label(self.Frame, text=title)
    label.pack(anchor=tk.W, padx=42) # 

    tree.pack(pady=10, padx=40)

    Button = tk.Button(self.Frame, text="detail")
    Button.bind("<Button-1>", self.child_window)
    Button.pack(anchor=tk.E, padx=42) # 
  
  def run(self):

    for title, df in zip(self.titles, self.dfs):
      self.treev(title, df)

    self.root.mainloop()

if __name__ == '__main__':

  r = Race()
  date_place, titles, dfs = r.entries()
  t = TkRaces(date_place, titles, dfs)
  t.run()