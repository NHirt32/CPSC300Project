import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from itertools import cycle
import time
import level_generator
import settings


def next_img(root, panel, images):
    img = next(images)
    img = Image.open(img)
    img = ImageTk.PhotoImage(img)
    panel.img = img
    panel['image'] = img
    root.after(150, next_img, root, panel, images)

def main():

    # Initiates pygame for level one
    def level_one():
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(1)
        settings.curr_level = 1

    # Initiates pygame for level two
    def level_two():
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(2)
        settings.curr_level = 2

    # Initiates pygame for level three
    def level_three():
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(3)
        settings.curr_level = 3

    # Initiates pygame for level four
    def level_four():
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(4)
        settings.curr_level = 4

    # Initiates pygame for level five
    def level_five():
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(5)
        settings.curr_level = 5

    # Used to change the difficulty of the game based on diff_scale
    def define_num_entities(diff_level):
        if diff_level == 1:
            return settings.easy_num
        elif diff_level == 2:
            return settings.mid_num
        else:
            return settings.hard_num

    root = tk.Tk()

    root.title("Phil the Candle")

    width = settings.menu_width
    height = settings.menu_height

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (settings.screen_width / 2) - (width / 2)
    y = (settings.screen_height / 2) - (height / 2)

    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.config(bg=settings.menu_colour)

    frame = tk.Frame(root, bg=settings.menu_colour)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    label = Label(frame, text="Phil The Candle!", bg=settings.menu_colour)
    label.config(font=("Impact", 40))
    label.grid(row=0, padx=10, pady=10, columnspan=5)

    images = ['assets/1_1.png', 'assets/1_2.png', 'assets/1_3.png', 'assets/2_1.png', 'assets/2_2.png',
              'assets/2_3.png']
    images = cycle(images)

    panel = tk.Label(frame, bg=settings.menu_colour)
    panel.grid(row=1, column=2)


    label = Label(frame, text="Difficulty Slider", bg=settings.menu_colour)
    label.config(font=("Impact", 18))
    label.grid(row=3, padx=10, pady=0, columnspan=5)

    diff_scale = Scale(frame, from_=1, to=3, orient=HORIZONTAL, bg=settings.menu_colour, length=120)
    diff_scale.grid(row=4, padx=10, pady=10, columnspan=5)

    button = tk.Button(frame, text="How To Play", font=('Impact', 18), height=1, width=15,
                       command=lambda: [how_to_menu()])
    button.grid(row=5, columnspan=5, padx=10, pady=10)

    button = tk.Button(frame, text="1", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_one(), root.destroy()])
    button.grid(row=6, column=0, padx=20, pady=20)

    button = tk.Button(frame, text="2", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_two(), root.destroy()])
    button.grid(row=6, column=1, padx=20, pady=20)

    button = tk.Button(frame, text="3", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_three(), root.destroy()])
    button.grid(row=6, column=2, padx=20, pady=20)

    button = tk.Button(frame, text="4", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_four(), root.destroy()])
    button.grid(row=6, column=3, padx=20, pady=20)

    button = tk.Button(frame, text="5", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_five(), root.destroy()])
    button.grid(row=6, column=4, padx=20, pady=20)

    root.after(140, next_img, root, panel, images)
    root.mainloop()


# Creates how to menu
def how_to_menu():
    ht_win = tk.Tk()
    ht_win.config(bg=settings.menu_colour)

    width = settings.ht_width
    height = settings.ht_height

    x = (settings.screen_width / 2) - (width / 2)
    y = (settings.screen_height / 2) - (height / 2)

    ht_win.geometry("%dx%d+%d+%d" % (width, height, x, y))
    ht_win.config(bg=settings.menu_colour)

    text_wid = Text(ht_win, padx=20, pady=20, font=('Arial, 18'), bg=settings.menu_colour)

    text_file = "How_To_Text.txt"

    with open(text_file, 'r') as f:
        text_wid.insert(INSERT, f.read())

    text_wid.pack()

    ht_win.mainloop()
