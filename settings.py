import level_generator
import random
from screeninfo import get_monitors

monitors = get_monitors()

screen_width = monitors[0].width
screen_height = monitors[0].height - 64

if (screen_height%2) != 0:
    screen_height -= 1

if (screen_width%2) != 0:
    screen_width -= 1

max_frames = 60
theme = 1
curr_level = 1

# How To Death defaults

ht_width = 550
ht_height = 450

# Pause Defaults
pause_width = 450
pause_height = 400
pause_status = 3

# Main Menu Defaults
menu_width = 550
menu_height = 450
menu_colour = "#00FFFF"

# Difficult Defaults
num_entities = 3
easy_num = 3
mid_num = 5
hard_num = 8

"""
levelM = [
    "00000O",
    "0X0000",
    "0X0000",
    "0X0000",
    "0X0000",
    "0X0P00",
    "XXXXXX"
]
"""

levelM = None

# level0 = level_generator.get_level(3)d

# levelM = [
#     "00000000X000000000000000000000000000000000000000000000000000000000000000000X00000000000000000000000000000000000000000000000000",
#     "00000000O0000000000000000000000000000000000000000000000000XXXX00XX000000000000000000000000X000X000000000000000000000000XX00000",
#     "0000X0FXXX0000000000XX0E0XX0000000XX000000000000000000XX00000E00000X00000X0X0X00000000000XX000XX0000000XX00000XX00000XXXX00000",
#     "0P0E00000E000XX00000XX0E0XX0E000E0XX000000000000000000000000X000000000000000E00E00E00000XXX000XXX0E00E0XX00000XX000XXXXXX00000",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX000XXXXXXXXXXX000XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX000XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX000XXXXXXXXXXX000XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX000XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#
# ]

