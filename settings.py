import level_generator
import random
tile_size = 192
screen_width = 8 * tile_size
screen_height = 5 * tile_size
max_frames = 60

level0 = level_generator.get_level(3)



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