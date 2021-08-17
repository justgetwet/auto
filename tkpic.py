import os
import tkinter as tk
from PIL import Image, ImageTk

if __name__ == '__main__':

	root = tk.Tk()
	root.title = "pic pic"
	w = 600
	h = 600
	root.geometry(f"{w}x{h}+200+50")
	canvas = tk.Canvas(root)
	canvas.grid(row=0, column=0)

	p = "./images/A-100_内山雄介.png"
	im = Image.open(p)
	img = ImageTk.PhotoImage(im)
	canvas.create_image(0, 0, anchor=tk.NW, image=img)

	root.mainloop()


	# jpg -> png 変換
	# 
	# p = "./images/A-1_岩崎亮一.jpg"
	# print(os.path.exists(p))

	# p = "./jpgs"
	# files = os.listdir(p)
	# for file in files:
	# 	jpg_file = "./jpgs/" + file
	# 	im = Image.open(jpg_file)
	# 	png_file = "./images/" + file.replace(".jpg", ".png")
	# 	im.save(png_file)

