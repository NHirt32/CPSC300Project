"""settings contains a large number of important fields that the game will read from."""

import level_generator
import random
from screeninfo import get_monitors

# Get screen sizes
monitors = get_monitors()

screen_width = monitors[0].width
screen_height = monitors[0].height - 64

if (screen_height % 2) != 0:
    screen_height -= 1

if (screen_width % 2) != 0:
    screen_width -= 1

max_frames = 60
theme = 1
curr_level = 1

# How To Screen defaults
ht_width = 600
ht_height = 450

# Pause menu defaults
pause_width = 450
pause_height = 400
pause_status = 3

# Score Menu Defaults
sc_width = 600
sc_height = 450

# Main Menu Defaults
menu_width = 600
menu_height = 450
menu_colour = "#00FFFF"

# Difficult Defaults
curr_difficulty = 1
num_entities = 3
easy_num = 3
mid_num = 5
hard_num = 8

# Game Win and Death Screens
score = 10000
death_penalty = 2500
kill_reward = 300
hurt_penalty = 300
start_time = 0
end_time = 0

# Player demo variables. Messing with these can break the game.
jump_power = 21  # Defines max jump power
gravity = -100  # Defines max fall speed. MUST BE NEGATIVE for proper behaviour.
slide_speed = -4  # defines gravity when sliding down a wall, MUST BE NEGATIVE for proper behaviour.
speed = 15  # Max momentum. MUST BE EVENLY DIVISIBLE BY horizontal_acceleration.
horizontal_acceleration = 3 # should be less than speed.
wall_jump_horizontal_momentum = 21  # Max wall jump horizontal momentum. MUST BE EVENLY DIVISIBLE BY
# horizontal_acceleration
wall_jump_vertical_momentum = 21  # Max wall jump vertical momentum.

levelM = None

