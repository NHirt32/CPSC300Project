import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
from itertools import cycle
import level_generator
import settings
import json


def next_img(root, panel, images):
    """TODO"""
    img = next(images)
    img = Image.open(img)
    img = ImageTk.PhotoImage(img)
    panel.img = img
    panel['image'] = img
    root.after(150, next_img, root, panel, images)


def main():
    """main() runs the main menu."""
    def level_one():
        """level_one() initiates pygame for level one."""
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(1)
        settings.curr_level = 1

    def level_two():
        """level_two() initiates pygame for level two."""
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(2)
        settings.curr_level = 2

    def level_three():
        """level_three() initiates pygame for level three."""
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(3)
        settings.curr_level = 3

    def level_four():
        """level_four() initiates pygame for level four."""
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(4)
        settings.curr_level = 4

    def level_five():
        """level_five() initiates pygame for level five."""
        settings.num_entities = define_num_entities(diff_scale.get())
        settings.levelM = level_generator.get_level(5)
        settings.curr_level = 5

    def define_num_entities(diff_level):
        """define_num_entities() is used to change the difficulty of the game based on diff_scale."""
        if diff_level == 1:
            settings.curr_difficulty = 1
            return settings.easy_num
        elif diff_level == 2:
            settings.curr_difficulty = 2
            return settings.mid_num
        else:
            settings.curr_difficulty = 3
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
    root.resizable(False, False)

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

    diff_scale = Scale(frame, from_=1, to=3, orient=HORIZONTAL, bg=settings.menu_colour, length=160)
    diff_scale.grid(row=4, padx=10, pady=5, columnspan=5)

    button = tk.Button(frame, text="How To Play", font=('Impact', 18), height=1, width=20,
                       command=lambda: [how_to_menu()])
    button.grid(row=5, columnspan=5, padx=10, pady=5)

    button = tk.Button(frame, text="High Scores", font=('Impact', 18), height=1, width=27,
                       command=lambda: [scoresMenu()])
    button.grid(row=6, columnspan=5, padx=10, pady=5)

    button = tk.Button(frame, text="1", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_one(), root.destroy()])
    button.grid(row=7, column=0, padx=20, pady=5)

    button = tk.Button(frame, text="2", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_two(), root.destroy()])
    button.grid(row=7, column=1, padx=20, pady=5)

    button = tk.Button(frame, text="3", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_three(), root.destroy()])
    button.grid(row=7, column=2, padx=20, pady=5)

    button = tk.Button(frame, text="4", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_four(), root.destroy()])
    button.grid(row=7, column=3, padx=20, pady=5)

    button = tk.Button(frame, text="5", font=('Impact', 18), height=1, width=4,
                       command=lambda: [level_five(), root.destroy()])
    button.grid(row=7, column=4, padx=20, pady=5)

    root.after(140, next_img, root, panel, images)
    root.mainloop()

def how_to_menu():
    """how_to_menu() creates how to menu."""
    ht_win = tk.Tk()
    ht_win.config(bg=settings.menu_colour)
    ht_win.title("How To Play!")
    ht_win.resizable(False, False)

    width = settings.ht_width
    height = settings.ht_height

    x = (settings.screen_width / 2) - (width / 2)
    y = (settings.screen_height / 2) - (height / 2)

    ht_win.geometry("%dx%d+%d+%d" % (width, height, x, y))
    ht_win.config(bg=settings.menu_colour)

    text_win = Text(ht_win, padx=20, pady=20, font=('Impact', 18), bg=settings.menu_colour)

    text_file = "How_To_Text.txt"

    with open(text_file, 'r') as f:
        text_win.insert(INSERT, f.read())

    text_win.config(state='disabled')
    text_win.pack()

    ht_win.mainloop()


def scoresMenu():
    """scoresMenu() creates and runs the scores menu."""
    sc_win = tk.Tk()
    sc_win.config(bg=settings.menu_colour)
    sc_win.title("High Scores")
    sc_win.resizable(False, False)

    width = settings.sc_width
    height = settings.sc_height

    x = (settings.screen_width / 2) - (width / 2)
    y = (settings.screen_height / 2) - (height / 2)

    sc_win.geometry("%dx%d+%d+%d" % (width, height, x, y))

    with open("scores.json") as jsonFile:
        data = json.load(jsonFile)

    text_win = Text(sc_win, padx=20, pady=20, font=('Impact', 18), bg=settings.menu_colour)

    text_win.insert(INSERT, "HIGH SCORES:       CANDLE              TORCH             BONFIRE")

    keys = ["1-1", "1-2", "1-3", "1-4", "1-5", "2-1", "2-2", "2-3", "2-4", "2-5", "3-1", "3-2", "3-3", "3-4", "3-5"]
    for i in range(6):
        if i == 0:
            continue
        else:
            text_win.insert(INSERT, ("\n\n        Level " + str(i) + ":         "))

        for x in keys:
            if x[2] == str(i):
                if data[x] == 0:
                    text_win.insert(tk.END, "                               ")

                else:
                    if (data[x] < 10000):
                        text_win.insert(tk.END, "        " + str(data[x]) + "           ")
                    else:
                        text_win.insert(tk.END, "      " + str(data[x]) + "           ")

    text_win.config(state='disabled')
    text_win.pack()

    sc_win.mainloop()
