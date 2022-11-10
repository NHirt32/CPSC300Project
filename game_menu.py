import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from itertools import cycle
import time

import level_generator
import settings

root = tk.Tk()

root.title("Phil the Candle")
root.geometry("500x400")
root.config(bg="#00FFFF")

frame = tk.Frame(root, bg='#00FFFF')
frame.place(relx=0.5, rely=0.5, anchor="center")

images = ['assets/1_1.png', 'assets/1_2.png', 'assets/1_3.png', 'assets/2_1.png', 'assets/2_2.png', 'assets/2_3.png']
images = cycle(images)

panel = tk.Label(frame)
panel.grid(row=0, column=2)


# bg=root.wm_attributes('-transparentcolor', 'white')
def next_img():
    img = next(images)
    img = Image.open(img)
    img = ImageTk.PhotoImage(img)
    panel.img = img
    panel['image'] = img


next_img()

btn_img = PhotoImage(file="assets/ground_block.png")

button = tk.Button(frame, i=btn_img, command=next_img)
button.grid(row=1, column=2, padx=20, pady=20)

button = tk.Button(frame, text="1", font=('Arial', 18), command=lambda: [level_one(), root.destroy()])
button.grid(row=2, column=0, padx=20, pady=20)

button = tk.Button(frame, text="2", font=('Arial', 18), command=lambda: [level_two(), root.destroy()])
button.grid(row=2, column=1, padx=20, pady=20)

button = tk.Button(frame, text="3", font=('Arial', 18), command=lambda: [level_three(), root.destroy()])
button.grid(row=2, column=2, padx=20, pady=20)

button = tk.Button(frame, text="4", font=('Arial', 18), command=lambda: [level_four(), root.destroy()])
button.grid(row=2, column=3, padx=20, pady=20)

button = tk.Button(frame, text="5", font=('Arial', 18), command=lambda: [level_five(), root.destroy()])
button.grid(row=2, column=4, padx=20, pady=20)


def level_one():
    settings.levelM = level_generator.get_level(1)


def level_two():
    settings.levelM = level_generator.get_level(2)


def level_three():
    settings.levelM = level_generator.get_level(3)


def level_four():
    settings.levelM = level_generator.get_level(4)


def level_five():
    settings.levelM = level_generator.get_level(5)


def main():
    root.mainloop()
