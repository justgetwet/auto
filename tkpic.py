import os
import tkinter as tk
from PIL import Image, ImageTk

if __name__ == '__main__':

  root = tk.Tk()
  root.title = "pic pic"
  w = 600
  h = 600
  root.geometry(f"{w}x{h}+200+50")
  colors = ["white", "black", "red", "blue", "yellow", "green", "orange"]
  imgs = []
  for i, c in zip(range(len(colors)), colors):
    canvas = tk.Canvas(root, height=63, width=60, bg=c)
    # canvas.grid(row=0, column=i)
    canvas.pack(side=tk.LEFT)

    p = "./images/A-100_内山雄介.png"
    im = Image.open(p)
    img = ImageTk.PhotoImage(im)
    imgs.append(img)
    canvas.create_image(3, 3, image=img, anchor=tk.NW)

  root.mainloop()


  # jpg -> png 変換
  # 
  # p = "./images/A-1_岩崎亮一.jpg"
  # print(os.path.exists(p))
  # 
  # p = "./jpgs"
  # files = os.listdir(p)
  # for file in files:
  # 	jpg_file = "./jpgs/" + file
  # 	im = Image.open(jpg_file)
  # 	png_file = "./images/" + file.replace(".jpg", ".png")
  # 	im.save(png_file)

