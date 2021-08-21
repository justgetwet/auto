import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from laps import Laps
from result import Result

class TkPlots:

  def __init__(self, yyyymmdd: str, place: str, race: int):
    self.root = tk.Tk()
    self.root.geometry("+150+50")
    laps = Laps(yyyymmdd, place, race)
    self.title = laps.raceTitle()
    self.srs_laps = laps.pickup_and_calc()

  def plots(self):

    self.fig = plt.figure(figsize=(12.0, 6.0))  # Figure
    rows = len(self.srs_laps)
    # fig.patch.set_facecolor('blue') 
    ax1 = self.fig.add_subplot(141)  # Axes
    ax1.set_title("last 10")
    ax1.patch.set_facecolor("gray")
    ax1.set_ylim(-100, 50)
    ax2 = self.fig.add_subplot(142)  # Axes
    ax2.set_title("same handicap")
    ax2.patch.set_facecolor("gray")
    ax2.set_ylim(-100, 50)
    ax3 = self.fig.add_subplot(143)  # Axes
    ax3.set_title("trial laps")
    ax3.patch.set_facecolor("gray")
    ax3.set_ylim(-200, 100)
    ax4 = self.fig.add_subplot(144)  # Axes
    ax4.set_title("start")
    ax4.patch.set_facecolor("gray")
    # ax4.set_ylim(-200, 100)
    xmin = 1
    xmax = rows
    ax1.hlines([0], xmin, xmax, "black", linestyles='dashed')
    ax2.hlines([0], xmin, xmax, "black", linestyles='dashed')
    ax3.hlines([0], xmin, xmax, "black", linestyles='dashed')
    colors = ["white", "black", "red", "blue", "yellow", "green", "hotpink"]
    # handis = []
    for sr, col in zip(self.srs_laps, colors[:rows]):
      n = sr["no"]
      avgDif = sr["avgDif"]
      lstDifs, eqhDifs, tryDifs, stDifs = sr["lstDifs"], sr["eqhDifs"], sr["tryDifs"], sr["StDifs"]
      tryDif, prdDif, runDif = sr["tryDif"], sr["prdDif"], sr["runDif"]
      x1 = [n for _ in range(len(lstDifs))]
      y1 = lstDifs
      x2 = [n for _ in range(len(eqhDifs))]
      y2 = eqhDifs
      x3 = [n for _ in range(len(tryDifs))]
      y3 = tryDifs
      x4 = [n for _ in range(len(stDifs))]
      y4 = stDifs
      ax1.plot(x1, y1, marker="o", linestyle="dashed", color=col)
      ax1.plot(n, avgDif, marker="D", markersize=9, color=col)
      ax2.plot(x2, y2, marker="o", linestyle="dashed", color=col)
      ax2.plot(n, avgDif, marker="D", markersize=9, color=col)
      ax3.plot(x3, y3, marker="o", linestyle="dashed", color=col)
      if not tryDif == 0.0:
        ax3.plot(n, tryDif, marker="D", markersize=9, color=col)
        ax3.plot(n, prdDif, marker="*", markersize=9, color=col)
      if not runDif == 0.0:
        ax3.plot(n, runDif, marker="x", markersize=9, color=col)
      ax4.plot(x4, y4, marker="o", linestyle="dashed", color=col)
      # handis.append(sr["handi"].strip("m"))
    # ax4.set_xticklabels(handis)

  def _destroyWindow(self):
    self.root.quit()
    self.root.destroy()

  def run(self):
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
  
  tkp =TkPlots('20210820','浜松', 9)
  tkp.run()
  # print(laps.raceTitle())
  # tpls = laps.select_latest_laps()
  # for tpl in tpls:
  #   print(tpl)