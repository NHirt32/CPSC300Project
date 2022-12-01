import random
import settings


def addEntities(level, path_coordinates, num_entities):
    """addEntities() adds walker characters, objective characters, and flier characters into an existing maze layout.

    :param level: a list of lists of characters that represents the maze layout.
    :param path_coordinates: a list of tuples representing coordinates in the maze path.
    :param num_entities: the maximum number of objective characters and enemy characters to generate in the maze layout
    """
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
    """isolated() determines whether a coordinate does not have any objective characters or enemy characters
     adjacent to itself.

    :param level: a list of lists of characters that represents the maze layout.
    :param coor: the tuple to check around.
    :returns: true if the coordinate does not have any objective characters or enemy characters
     adjacent to itself."""
    if level[coor[0]][coor[1]] == '0':
        if level[coor[0] - 1][coor[1]] == '0' or level[coor[0] - 1][coor[1]] == 'X':
            if level[coor[0] + 1][coor[1]] == '0' or level[coor[0] + 1][coor[1]] == 'X':
                if level[coor[0]][coor[1] - 1] == '0' or level[coor[0]][coor[1] - 1] == 'X':
                    if level[coor[0]][coor[1] + 1] == '0' or level[coor[0]][coor[1] + 1] == 'X':
                        return True
    return False

def not_boxed(level, coor):
    """not_boxed() determines whether a coordinate has walls on its left and right.

    :param level: a list of lists of characters that represents the maze layout.
    :param coor: the tuple to check around.
    :returns: true if the coordinate has walls on its left and right."""
    return level[coor[0]][coor[1] - 1] != 'X' or level[coor[0]][coor[1] + 1] != 'X'

def has_ground(level, coor):
    """has_ground() determines whether a coordinate has ground just beneath itself.

    :param level: a list of lists of characters that represents the maze layout.
    :param coor: the tuple to check around.
    :returns: true if the coordinate has ground just beneath itself."""
    return level[coor[0] + 1][coor[1]] == 'X'

def has_ground_around(level, coor):
    """has_ground_around() determines whether a coordinate has ground beneath itself,
    diagonally left beneath itself, and diagonally right beneath itself..

    :param level: a list of lists of characters that represents the maze layout.
    :param coor: the tuple to check around.
    :returns: true if the coordinate has ground beneath itself,
    diagonally left beneath itself, and diagonally right beneath itself."""
    return level[coor[0] + 1][coor[1]] == 'X' and level[coor[0] + 1][coor[1] + 1] == 'X' and \
           level[coor[0] + 1][coor[1] - 1] == 'X'


# This should be the only real method that you guys need to deal with
# Will return the correct level based upon the number passed to it
def get_level(level_num):
    """get_level() generates a maze layout and adds entities to it.

    :param level_num: an integer representing the type of level to generate, the level's theme.
    :returns: a list of strings representing the maze layout with enemies."""
    level = get_format_tileset(level_num)
    path_coordinates = []

    # Start of path and player spawn
    if level_num == 1:
        create_level_path(level, path_coordinates, 1, 1)
        level[1][1] = 'P'
    elif level_num == 2:
        create_level_path(level, path_coordinates, 1, 1)
        level[1][1] = 'P'
    elif level_num == 3:
        create_level_path(level, path_coordinates, 1, 4)
        level[1][4] = 'P'
    elif level_num == 4:
        create_level_path(level, path_coordinates, 1, 5)
        level[1][5] = 'P'
    elif level_num == 5:
        create_level_path(level, path_coordinates, 4, 4)
        level[4][4] = 'P'


    path_coordinates.pop(0)
    addEntities(level, path_coordinates, settings.num_entities)

    return convert_format(level)

def get_format_tileset(level_num):
    """get_format_tileset() grabs a suitable layout to carve for tilesets.

    :param level_num: an integer representing the type of level to generate, the level's theme.
    :returns: a list of lists of characters representing the maze layout to carve."""
    if level_num == 1:
        return [['X' for x in range(10)] for y in range(4)]

    elif level_num == 2:
        stair = [['X', 'X', 'X', 'X', '0', '0'],
                 ['X', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', 'X', 'X'],
                 ['0', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', 'X', 'X'],
                 ['X', 'X', 'X', 'X', '0', '0'],
                 ]

        return stair

    elif level_num == 3:
        tunnel = [['0', '0', '0', 'X', 'X', 'X', '0', '0', '0'],
                  ['0', '0', '0', 'X', 'X', 'X', '0', '0', '0'],
                  ['0', '0', '0', 'X', 'X', 'X', '0', '0', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
                  ]
        return tunnel

    elif level_num == 4:
        return [['X' for x in range(10)] for y in range(5)]
        # return [['X', 'X', 'X', 'X', 'X', 'X', 'X'],
        #         ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
        #         ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
        #         ['X', 'X', 'X', 'X', 'X', 'X', 'X'],
        #         ['X', 'X', 'X', 'X', 'X', 'X', 'X']]

    elif level_num == 5:
        level5 = [
            ['0', '0', '0', '0', 'X', '0', '0', '0', '0'],
            ['0', '0', '0', 'X', 'X', 'X', '0', '0', '0'],
            ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
            ['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'],
            ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
            ['0', 'X', 'X', 'X', 'X', 'X', 'X', 'X', '0'],
            ['0', '0', 'X', 'X', 'X', 'X', 'X', '0', '0'],
            ['0', '0', '0', 'X', 'X', 'X', '0', '0', '0'],
            ['0', '0', '0', '0', 'X', '0', '0', '0', '0']]

        return level5
    return -1

def get_format(level_num):
    """get_format() grabs a suitable layout to carve for mazes. No longer in use with tile-set system.

    :param level_num: an integer representing the type of level to generate, the level's theme.
    :returns: a list of lists of characters representing the maze layout to carve."""
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

def convert_format(level):
    """convert_format() converts the format of the level so that it is usable by the level_renderer.

    :param level: a list of lists of characters representing the carved maze layout.
    :returns: a list of strings representing the maze layout."""
    converted = []
    for i in range(len(level)):
        level[i] = array_to_string(level[i])
    return level

def array_to_string(char_array):
    """array_to_string() converts an array of characters to a string.

    :param char_array: the list of characters to convert.
    :returns: the newly-formed string."""
    temp = ""
    for x in char_array:
        temp += x
    return temp

def create_level_path(level, path_coordinates, row, col):
    """create_level_path() is the actual algorithm that cuts the path and randomly generates the level.

    :param level: the list of lists of characters that represent the level to be carved.
    :param path_coordinates: an empty list to store the path coordinates in the maze.
    :param row: an integer representing the starting row to carve at.
    :param col: an integer representing the starting col to carve at."""
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

def is_valid_up(level, row, col):
    """is_valid_up() checks to see if carving up at a coordinate is a valid option in generating a path in the maze.

    :param level: the list of lists of characters that represent the level being carved.
    :param row: the row of the coordinate to check at.
    :param col: the col of the coordinate to check at.
    :returns: true if carving up at a coordinate is a valid option in generating a path in the maze."""
    if 1 < row:
        if level[row - 1][col] != '0' and level[row - 2][col] != '0':
            if level[row - 1][col - 1] != '0' and level[row - 1][col + 1] != '0':
                return True
    else:
        return False

def is_valid_right(level, row, col):
    """is_valid_right() checks to see if carving up at a coordinate is a valid option in generating a path in the maze.

    :param level: the list of lists of characters that represent the level being carved.
    :param row: the row of the coordinate to check at.
    :param col: the col of the coordinate to check at.
    :returns: true if carving right at a coordinate is a valid option in generating a path in the maze."""
    if col < len(level[0]) - 2:
        if level[row][col + 1] != '0' and level[row][col + 2] != '0':
            if level[row - 1][col + 1] != '0' and level[row + 1][col + 1] != '0':
                return True
    else:
        return False

def is_valid_down(level, row, col):
    """is_valid_down() checks to see if carving down at a coordinate is a valid option in generating a path in the maze.

    :param level: the list of lists of characters that represent the level being carved.
    :param row: the row of the coordinate to check at.
    :param col: the col of the coordinate to check at.
    :returns: true if carving down at a coordinate is a valid option in generating a path in the maze."""
    if row < len(level) - 2:
        if level[row + 1][col] != '0' and level[row + 2][col] != '0':
            if level[row + 1][col - 1] != '0' and level[row + 1][col + 1] != '0':
                return True
    else:
        return False

def is_valid_left(level, row, col):
    """is_valid_left() checks to see if carving left at a coordinate is a valid option in generating a path in the maze.

    :param level: the list of lists of characters that represent the level being carved.
    :param row: the row of the coordinate to check at.
    :param col: the col of the coordinate to check at.
    :returns: true if carving left at a coordinate is a valid option in generating a path in the maze."""
    if 1 < col:
        if level[row][col - 1] != '0' and level[row][col - 2] != '0':
            if level[row - 1][col - 1] != '0' and level[row + 1][col - 1] != '0':
                return True
    else:
        return False


# Prints the level to the console for the purpose of testing
def print_level(level):
    """ print_level() prints the level to the console for the purpose of testing.

    :param level: the list of lists of characters that represent the level."""
    col_len = len(level[0])
    row_len = len(level)

    for i in range(len(level)):
        print()
        for j in range(len(level[0])):
            print(level[i][j], end="")
