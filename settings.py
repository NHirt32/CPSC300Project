import level_generator
import random


screen_width = 1000
screen_height = 800
max_frames = 60

level0 = [
    "B",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
    "0000000000000000000000000000000000000",
    "0000000000000000000000000000000000000",
    "000000000000000000000000000000P000000",
    "000000000000000000000000XXXXXXXX000XX",
    "000000000000000000000000XXXXXXXX0E0XX",
    "000000000000000000000000XXXXXXXXXXXXX",
]

# level0 = level_generator.get_level(3)


# level0 = [
#    "B0000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000A00000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "00000000000000000000000000P00000000000000000000000000000",
#    "00000000000000000000000000000000000000000000000000000000",
#    "0000000000000000000000CTTTTTTTH0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000",
#    "0000000000000000000000LXXXXXXXR0000000000000000000000000"
#    ]