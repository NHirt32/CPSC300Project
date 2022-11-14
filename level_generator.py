import random


def addEntities(level, num):
    col_len = len(level[0])
    row_len = len(level)
    for i in range(num):
        row = random.randrange(2,row_len - 1)
        col = random.randrange(2,col_len)
        if level[row+1][col] == '0':
            level[row][col] = 'F'
        else:
            level[row][col] = 'E'

# This should be the only real method that you guys need to deal with
# Will return the correct level based upon the number passed to it
def get_level(level_num):
    level = get_format(level_num)

    if level_num == 1:
        create_level_path(level, 4, 1)
        addEntities(level, 3)
        level[4][1] = 'P'
    elif level_num == 2:
        create_level_path(level, 1, 3)
        addEntities(level, 2)
        level[1][1] = 'P'
    elif level_num == 3:
        create_level_path(level, 0, 3)
        addEntities(level, 3)
        level[0][4] = 'P'
    elif level_num == 4:
        create_level_path(level, 1, 3)
        addEntities(level, 3)
        level[1][1] = 'P'
    elif level_num == 5:
        create_level_path(level, 1, 6)
        addEntities(level, 3)
        level[1][6] = 'P'

    return convert_format(level)


# Defines the format for the level
def get_format(level_num):
    if level_num == 1:
        return [['X' for x in range(40)] for y in range(6)]

    elif level_num == 2:
        stair = [['X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X'],
                 ]

        return stair

    elif level_num == 3:
        tunnel = [['0', '0', '0', 'X', 'X', 'X', '0', '0', '0'] for x in range(15)]
        cavern = [['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'] for t in range(50)]
        return tunnel + cavern

    elif level_num == 4:
        return [['X' for x in range(50)] for y in range(5)]

    elif level_num == 5:
        level5 = [['0', '0', '0', '0', '0', '0', 'X', '0', '0', '0', '0', '0', '0'],
                  ['0', '0', '0', '0', '0', 'X', 'X', 'X', '0', '0', '0', '0', '0'],
                  ['0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0'],
                  ['0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'],
                  ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
                  ['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ['0', '0', '0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0', '0', '0'],
                  ['0', '0', '0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0', '0', '0'],
                  ['0', '0', '0', '0', '0', 'X', 'X', 'X', '0', '0', '0', '0', '0'],
                  ['0', '0', '0', '0', '0', '0', 'X', '0', '0', '0', '0', '0', '0']
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
def create_level_path(level, row, col):
    # Mark the passed cell as visited
    level[row][col] = '0'

    # Used to choose direction in level generation
    direction = [0, 1, 2, 3]
    random.shuffle(direction)

    while direction:
        temp = direction.pop()
        # Move Up
        if temp == 0 and is_valid_up(level, row, col):
            level[row - 1][col] = '0'
            create_level_path(level, row - 1, col)
        # Move Right
        if temp == 1 and is_valid_right(level, row, col):
            level[row][col + 1] = '0'
            create_level_path(level, row, col + 1)
        # Move Down
        if temp == 2 and is_valid_down(level, row, col):
            level[row + 1][col] = '0'
            create_level_path(level, row + 1, col)
        # Move Left
        if temp == 3 and is_valid_left(level, row, col):
            level[row][col - 1] = '0'
            create_level_path(level, row, col - 1)


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
