import tkinter as tk
from tkinter import *
import level_generator
import settings


def main():
    """main() creates and runs the pause menu."""

    # Initialize the tkinter window
    root = tk.Tk()
    root.title("Phil the Candle")
    width = settings.pause_width
    height = settings.pause_height
    x = (settings.screen_width / 2) - (width / 2)
    y = (settings.screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.config(bg=settings.menu_colour)

    # Initialize organizational frame
    frame = tk.Frame(root, bg=settings.menu_colour)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Add title to the frame
    title = Label(frame, text="Pause Menu", bg=settings.menu_colour)
    title.config(font=("Impact", 40))
    title.grid(row=0, padx=10, pady=10, columnspan=3)

    # Add Regenerate Level button
    button = tk.Button(frame, text="Regenerate Level", font=('Impact', 18), command=lambda: [regen_level(), root.destroy()])
    button.grid(row=1, column=1, padx=10, pady=10)

    # Add Main Menu button
    button = tk.Button(frame, text="Main Menu", font=('Impact', 18), command=lambda: [main_menu(), root.destroy()])
    button.grid(row=2, column=1, padx=10, pady=10)

    # Add Continue button
    button = tk.Button(frame, text="Continue", font=('Impact', 18), command=lambda: [cont(), root.destroy()])
    button.grid(row=3, column=1, padx=10, pady=10)

    # Add Quit Button
    button = tk.Button(frame, text="Quit", font=('Impact', 18), command=lambda: [quit(), root.destroy()])
    button.grid(row=4, column=1, padx=10, pady=10)

    root.mainloop()


def regen_level():
    """regen_level() regenerates the underlying maze layout of the layout."""
    settings.levelM = level_generator.get_level(settings.curr_level)
    settings.pause_status = 0


def main_menu():
    """main_menu() sets up variables to go to main menu."""
    settings.pause_status = 1


def quit():
    """quit() sets up variables to quit the game."""
    settings.pause_status = 2


def cont():
    """cont() sets up variables close the pause menu and continue the game."""
    settings.pause_status = 3
