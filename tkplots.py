import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from laps import Laps

class TkPlots:

  def __init__(self, yyyymmdd: str, place: str, race: int):
    self.root = tk.Tk()
    laps = Laps(yyyymmdd, place, race)
    self.title = laps.raceTitle()
    self.laps = laps.select_latest_laps()

  def plots(self):

    colors = ["white", "black", "red", "blue", "yellow", "green", "hotpink"]
    self.fig = plt.figure(figsize=(12.0, 6.0))  # Figure
    # fig.patch.set_facecolor('blue') 
    ax1 = self.fig.add_subplot(131)  # Axes
    ax1.set_title("last 10")
    ax1.patch.set_facecolor("gray")
    ax1.set_ylim(-100, 50)
    ax2 = self.fig.add_subplot(132)  # Axes
    ax2.set_title("same handicap")
    ax2.patch.set_facecolor("gray")
    ax2.set_ylim(-100, 50)
    ax3 = self.fig.add_subplot(133)  # Axes
    ax3.set_title("trial laps")
    ax3.patch.set_facecolor("gray")
    ax3.set_ylim(-200, 100)
    xmin = 1
    xmax = len(self.laps)
    ax1.hlines([0], xmin, xmax, "black", linestyles='dashed')
    ax2.hlines([0], xmin, xmax, "black", linestyles='dashed')
    for tp, col in zip(self.laps, colors):
      x1 = [tp[0] for _ in range(len(tp[5]))]
      y1 = tp[5]
      x2 = [tp[0] for _ in range(len(tp[6]))]
      y2 = tp[6]
      x3 = [tp[0] for _ in range(len(tp[7]))]
      y3 = tp[7]
      ax1.plot(x1, y1, marker="o", linestyle="dashed", color=col)
      ax1.plot(tp[0], tp[4], marker="D", markersize=9, color=col)
      ax2.plot(x2, y2, marker="o", linestyle="dashed", color=col)
      ax2.plot(tp[0], tp[4], marker="D", markersize=9, color=col)
      ax3.plot(x3, y3, marker="o", linestyle="dashed", color=col)
      ax3.plot(tp[0], tp[8], marker="D", markersize=9, color=col)
      ax3.plot(tp[0], tp[9], marker="s", markersize=9, color=col)

  def _destroyWindow(self):
    self.root.quit()
    self.root.destroy()

  def tkplots(self):
    self.plots()
    self.root.withdraw()
    self.root.title(self.title)
    self.root.protocol('WM_DELETE_WINDOW', self._destroyWindow)  # When you close the tkinter window.

    # Canvas
    canvas = FigureCanvasTkAgg(self.fig, master=self.root)  # Generate canvas instance, Embedding fig in root
    canvas.draw()
    canvas.get_tk_widget().pack()
    #canvas._tkcanvas.pack()

    # root
    self.root.update()
    self.root.deiconify()
    self.root.mainloop()

if __name__ == '__main__':
  
  tkp =TkPlots('20210820','浜松', 10)
  tkp.tkplots()
  # print(laps.raceTitle())
  # tpls = laps.select_latest_laps()
  # for tpl in tpls:
  #   print(tpl)