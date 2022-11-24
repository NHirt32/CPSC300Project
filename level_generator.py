import random

import settings


def addEntities(level, path_coordinates, num_entities):
    num_enemies = 0
    num_objectives = 0

    random.shuffle(path_coordinates)

    # Place isolated objectives
    for coor in path_coordinates:
        if num_objectives >= num_entities:
            break
        # Only place if it is a path
        if isolated(level, coor):
            level[coor[0]][coor[1]] = 'O'
            path_coordinates.remove(coor)
            num_objectives += 1

    # Place remaining objectives.
    while (num_objectives < num_entities) and not (len(path_coordinates) == 0):
        coor = path_coordinates.pop()
        level[coor[0]][coor[1]] = 'O'
        num_objectives += 1

    # Place isolated enemies, one iteration through path_coordinates.
    for coor in path_coordinates:
        if num_enemies >= num_entities:
            break
        # Only place if it is a path
        if isolated(level, coor):
            # Done place enemies inbetween walls
            if not_boxed(level, coor):
                # Change the ground cases for varied probability.
                if not has_ground(level, coor):
                    level[coor[0]][coor[1]] = 'F'
                    path_coordinates.remove(coor)
                    num_enemies += 1
                else:
                    level[coor[0]][coor[1]] = 'E'
                    path_coordinates.remove(coor)
                    num_enemies += 1

    # Place remaining enemies. Change the ground cases for varied probability.
    while (num_enemies < num_entities) and not (len(path_coordinates) == 0):
        coor = path_coordinates.pop()
        if not has_ground(level, coor):
            level[coor[0]][coor[1]] = 'F'
            num_enemies += 1
        else:
            level[coor[0]][coor[1]] = 'E'
            num_enemies += 1

    # Convert the rest to path characters.
    for coor in path_coordinates:
        if level[coor[0]][coor[1]] != 'P':
            level[coor[0]][coor[1]] = 'I'

def isolated(level, coor):
    if level[coor[0]][coor[1]] == '0':
        if level[coor[0] - 1][coor[1]] == '0' or level[coor[0] - 1][coor[1]] == 'X':
            if level[coor[0] + 1][coor[1]] == '0' or level[coor[0] + 1][coor[1]] == 'X':
                if level[coor[0]][coor[1] - 1] == '0' or level[coor[0]][coor[1] - 1] == 'X':
                    if level[coor[0]][coor[1] + 1] == '0' or level[coor[0]][coor[1] + 1] == 'X':
                        return True
    return False

def not_boxed(level, coor):
    return level[coor[0]][coor[1] - 1] != 'X' or level[coor[0]][coor[1] + 1] != 'X'

# Looks directly below coord.
def has_ground(level, coor):
    return level[coor[0] + 1][coor[1]] == 'X'

# Looks directly below, below and left, and below and right.
def has_ground_around(level, coor):
    return level[coor[0] + 1][coor[1]] == 'X' and level[coor[0] + 1][coor[1] + 1] == 'X' and \
           level[coor[0] + 1][coor[1] - 1] == 'X'


# This should be the only real method that you guys need to deal with
# Will return the correct level based upon the number passed to it
def get_level(level_num):
    level = get_format(level_num)
    path_coordinates = []

    if level_num == 1:
        create_level_path(level, path_coordinates, 1, 1)
        level[1][1] = 'P'
    elif level_num == 2:
        create_level_path(level, path_coordinates, 1, 1)
        level[1][1] = 'P'
    elif level_num == 3:
        create_level_path(level, path_coordinates, 1, 3)
        level[1][4] = 'P'
        level[1][3] = 'X'
    elif level_num == 4:
        create_level_path(level, path_coordinates, 1, 4)
        level[1][3] = 'P'
    elif level_num == 5:
        create_level_path(level, path_coordinates, 1, 10)
        level[1][10] = 'P'

    path_coordinates.pop(0)
    addEntities(level, path_coordinates, settings.num_entities)

    return convert_format(level)


# Defines the format for the level
def get_format(level_num):
    if level_num == 1:
        return [['X' for x in range(30)] for y in range(5)]

    elif level_num == 2:
        stair = [['X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                 ]

        return stair

    elif level_num == 3:
        tunnel = [['0', '0', '0', 'X', 'X', 'X', '0', '0', '0'] for x in range(10)]
        cavern = [['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'] for t in range(30)]
        return tunnel + cavern

    elif level_num == 4:
        return [['X' for x in range(30)] for y in range(5)]

    elif level_num == 5:
        level5 = [
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0'],
            ['0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0'],
            ['0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0'],
            ['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'],
            ['0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0'],
            ['0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0'],
            ['0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
            ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
        ]

        return level5
    return -1


# Converts the format of the level so that it is usable by the level_renderer
def convert_format(level):
    converted = []
    for i in range(len(level)):
        level[i] = array_to_string(level[i])
    return level


# Converts an array of characters to a string
def array_to_string(char_array):
    temp = ""
    for x in char_array:
        temp += x
    return temp


# Actual algorithm that cuts the path and randomly generates the level
def create_level_path(level, path_coordinates, row, col):
    # Mark the passed cell as visited
    level[row][col] = '0'
    path_coordinates.append((row, col))

    # Used to choose direction in level generation
    direction = [0, 1, 2, 3]
    random.shuffle(direction)

    while direction:
        temp = direction.pop()
        # Move Up
        if temp == 0 and is_valid_up(level, row, col):
            level[row - 1][col] = '0'
            create_level_path(level, path_coordinates, row - 1, col)
        # Move Right
        if temp == 1 and is_valid_right(level, row, col):
            level[row][col + 1] = '0'
            create_level_path(level, path_coordinates, row, col + 1)
        # Move Down
        if temp == 2 and is_valid_down(level, row, col):
            level[row + 1][col] = '0'
            create_level_path(level, path_coordinates, row + 1, col)
        # Move Left
        if temp == 3 and is_valid_left(level, row, col):
            level[row][col - 1] = '0'
            create_level_path(level, path_coordinates, row, col - 1)


# Checks to see if the level path can be cut up
def is_valid_up(level, row, col):
    if 1 < row:
        if level[row - 1][col] != '0' and level[row - 2][col] != '0':
            if level[row - 1][col - 1] != '0' and level[row - 1][col + 1] != '0':
                return True
    else:
        return False


# Checks to see if the level path can be cut right
def is_valid_right(level, row, col):
    if col < len(level[0]) - 2:
        if level[row][col + 1] != '0' and level[row][col + 2] != '0':
            if level[row - 1][col + 1] != '0' and level[row + 1][col + 1] != '0':
                return True
    else:
        return False


# Checks to see if the level path can be cut down
def is_valid_down(level, row, col):
    if row < len(level) - 2:
        if level[row + 1][col] != '0' and level[row + 2][col] != '0':
            if level[row + 1][col - 1] != '0' and level[row + 1][col + 1] != '0':
                return True
    else:
        return False


# Checks to see if the level path can be cut left
def is_valid_left(level, row, col):
    if 1 < col:
        if level[row][col - 1] != '0' and level[row][col - 2] != '0':
            if level[row - 1][col - 1] != '0' and level[row + 1][col - 1] != '0':
                return True
    else:
        return False


# Prints the level to the console for the purpose of testing
def print_level(level):
    col_len = len(level[0])
    row_len = len(level)

    for i in range(len(level)):
        print()
        for j in range(len(level[0])):
            print(level[i][j], end="")
