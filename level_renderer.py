from tile import *
from player import *
from animation import *
from walker import *
from flier import *
import tile_sets
import random

class LevelRenderer:
    """The LevelRenderer class contains all the objects found in a level and functions to draw them to the screen.
    It also provides the functionality to render the tile sets."""
    def __init__(self, screen, level_layout, theme):
        """Constructor for a LevelRenderer.

        :param screen: the screen to draw on.
        :param level_layout: the list of strings representing a level layout.
        :param theme: an integer representing the theme of the level."""
        # Render Groups
        self.animations = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.non_solids = pygame.sprite.Group()
        self.objectives = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()

        # Group combinations
        self.p_solids = pygame.sprite.Group()
        self.e_solids = pygame.sprite.Group()

        # Variables
        self.screen = screen
        self.level_layout = level_layout
        self.background_speed = 0.1
        self.theme = theme
        # Remember, a chosen tile_size should be evenly divisible by all assets that
        # are drawn using the fill() function in level renderer
        self.tile_size = settings.tile_size
        # Must be a multiple of tile size. We are using 5 by 5 tile sets.
        self.tileset_size = 5 * self.tile_size

        # Add any further sprite groups that need camera offset into this array.
        # The order of drawing is from left to right.
        self.all_tiles = [self.backgrounds, self.solids, self.non_solids, self.objectives, self.enemies, self.players,
                          self.effects]

        for string in level_layout:
            print(string)

        print("\n")

        # Drawing the layout to the screen
        for row in range(0, len(level_layout)):
            for col in range(0, len(level_layout[row])):

                position = ((col * self.tileset_size), (row * self.tileset_size))

                # Add cases here for different types of tiles.
                if level_layout[row][col] == 'P':
                    self.draw_player_tileset(position, row, col)

                elif level_layout[row][col] == 'E':
                    self.draw_walker_tileset(position, row, col)

                elif level_layout[row][col] == 'F':
                    self.draw_flier_tileset(position, row, col)

                elif level_layout[row][col] == 'Y':
                    self.draw_block_animation(position, self.theme)

                elif level_layout[row][col] == 'N':
                    self.draw_non_solid(position, self.theme)

                elif level_layout[row][col] == 'A':
                    self.draw_non_solid_animation(position, self.theme)

                elif level_layout[row][col] == 'O':
                    self.draw_objective_tileset(position, row, col)

                elif level_layout[row][col] == 'I':
                    self.draw_tileset(position, row, col)

        # Draw the background appropriate for the level's theme.
        self.draw_background(self.theme)

        # Need to move the camera over the player at the start, otherwise there may be an awkward offset
        init = (self.players.sprites()[0].rect.x, self.players.sprites()[0].rect.y)

        # The offset is reversed with its tuples, can simply use update to draw them
        self.update((settings.screen_width / 2, settings.screen_height / 2), init)

    def update(self, init_pos, final_pos):
        """update() redraws everything in the level in the proper order. It also handles moving everything for the
        camera.

        :param init_pos: a tuple representing the inital position of center of the last frame.
        :param final_pos: a tuple representing the final position of the center of the last frame."""
        # Intended to be physical distance that the player moved this frame,
        # stored as a tuple, (x,y).
        # Since directions are flipped, need to multiply by -1.
        change = (-1 * (final_pos[0] - init_pos[0]), -1 * (final_pos[1] - init_pos[1]))

        # For all groups within a level, the change must be calculated.
        # any further group must be factored in here, though I doubt we will
        # need more than that. Just add subsequent groups into the all_tiles array.
        # We could make the background a little dynamic,
        # perhaps make it move at fraction the rate of everything else for a perceived depth.

        self.screen.fill("white")

        back_elements = self.backgrounds.sprites()

        for element in back_elements:
            # Needs to use the center value for each rect coord, otherwise the camera possesses a small offset
            element.rect.centerx += ((change[0]) * self.background_speed)
            element.rect.centery += ((change[1]) * self.background_speed)

        for group in self.all_tiles:
            sprites = group.sprites()
            for sprite in sprites:
                sprite.rect.centerx += change[0]
                sprite.rect.centery += change[1]

        self.screen.fill("white")  # This shows when no background is present.

        # Drawing all sprites in the group to screen.
        self.backgrounds.draw(self.screen)
        self.solids.draw(self.screen)
        self.non_solids.draw(self.screen)
        self.objectives.draw(self.screen)
        self.enemies.draw(self.screen)
        self.players.draw(self.screen)
        self.effects.draw(self.screen)


    # Handlers for the level renderer, looks at the theme of the level and chooses what version to draw,
    # adds the constructed group to be drawn.
    def draw_player(self, position, theme):
        """draw_player() places a player in the level.

        :param position: a tuple representing the spot to put the player.
        :param theme: an integer representing the theme of the level."""
        player1 = Player(position)
        player1.add(self.players)  # Adds player1 to renderer group
        player1.add(self.animations)
        player1.add(self.e_solids)
        flame = \
            Animation([["assets/flame1_1.png", "assets/flame1_2.png", "assets/flame1_1.png", "assets/flame1_3.png"]],
                      position)
        flame.add(self.effects)
        flame.add(self.animations)

        # easy
        if theme == 1:
            vignette = Tile("assets/dark5.png", position)
            vignette.add(self.effects)

        # medium
        elif theme == 2:
            vignette = Tile("assets/dark3.png", position)
            vignette.add(self.effects)

        # hard
        elif theme == 3:
            vignette = Tile("assets/dark1.png", position)
            vignette.add(self.effects)

    def draw_walker(self, position, theme):
        """draw_walker() places a walker in the level.

        :param position: a tuple representing the spot to put the walker.
        :param theme: an integer representing the theme of the level."""
        enemy1 = Walker(position)
        enemy1.add(self.enemies)
        enemy1.add(self.animations)
        enemy1.add(self.p_solids)

    def draw_flier(self, position, theme):
        """draw_flier() places a flier in the level.

        :param position: a tuple representing the spot to put the flier.
        :param theme: an integer representing the theme of the level."""
        enemy1 = Flier(position)
        enemy1.add(self.enemies)
        enemy1.add(self.animations)
        enemy1.add(self.p_solids)

    def draw_block(self, position, theme):
        """draw_block() places a block in the level.

        :param position: a tuple representing the spot to put the block.
        :param theme: an integer representing the theme of the level."""
        rnd = random.randint(1, 100)

        # Jungle
        if theme == 1:
            asset_size = 192
            # Block probabilities for the jungles
            if rnd <= 10:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/jungle3.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 10 < rnd <= 50:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/jungle2.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 50 < rnd <= 100:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/jungle1.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)

        # Cave
        elif theme == 2:
            asset_size = 192
            # Block probabilities for the caves
            if rnd <= 2:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/cave3.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 2 < rnd <= 50:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/cave2.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 50 < rnd <= 100:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/cave1.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)

        # Ice
        elif theme == 3:
            asset_size = 192
            # Block probabilities for the ices
            if rnd <= 25:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/ice3.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 25 < rnd <= 50:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/ice2.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 50 < rnd <= 100:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/ice1.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)

        # Volcanic
        elif theme == 4:
            asset_size = 192
            # Block probabilities for the volcanics
            if rnd <= 6:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/volcanic3.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 6 < rnd <= 50:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/volcanic2.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 50 < rnd <= 100:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/volcanic1.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)

        # Ancient
        elif theme == 5:
            asset_size = 192
            # Block probabilities for the ancients
            if rnd <= 2:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/ancient3.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 2 < rnd <= 12:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/ancient2.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)
            elif 12 < rnd <= 100:
                blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile",
                                   "assets/ancient1.png")
                for block in blocks:
                    block.add(self.solids)
                    block.add(self.e_solids)
                    block.add(self.p_solids)

    def draw_block_animation(self, position, theme):
        """Currently unused. draw_block_animation() would place a block animation in the level.

        :param position: a tuple representing the spot to put block animation.
        :param theme: an integer representing the theme of the level."""
        if theme == 0:
            block = Animation([["assets/green_block.png", "assets/red_block.png"]], position)
            block.add(self.solids)
            block.add(self.e_solids)
            block.add(self.p_solids)
            block.add(self.animations)

    # Places background at specific location
    # Not all of them are centered, they just look ok where they are
    def draw_background(self, theme):
        """draw_background() places a background in the level.

        :param theme: an integer representing the theme of the level."""
        renderpoint = (0, 0)
        if theme == 1:
            background = Tile("assets/background_jungle.png", renderpoint)
            background.rect.topleft = renderpoint
            background.add(self.backgrounds)
        elif theme == 2:
            background = Tile("assets/background_cave.png", renderpoint)
            background.rect.topleft = renderpoint
            background.add(self.backgrounds)
        elif theme == 3:
            background = Tile("assets/background_ice.png", renderpoint)
            background.rect.topleft = renderpoint
            background.add(self.backgrounds)
        elif theme == 4:
            background = Tile("assets/background_volcanic.png", renderpoint)
            background.rect.topleft = renderpoint
            background.add(self.backgrounds)
        elif theme == 5:
            background = Tile("assets/background_ancient.png", renderpoint)
            background.rect.center = self.players.sprites()[0].rect.center
            background.add(self.backgrounds)

    def draw_non_solid(self, position, theme):
        """Currently unused. draw_non_solid() would place a generic non-solid in the level.

        :param position: a tuple representing the spot to put block non-solid.
        :param theme: an integer representing the theme of the level."""
        if theme == 0:
            non_solid = Tile("assets/red_cross.png", position)
            non_solid.add(self.non_solids)

    def draw_non_solid_animation(self, position, theme):
        """Currently unused. draw_non_solid_animation() would place a non-solid animation in the level.

        :param position: a tuple representing the spot to put non-solid animation.
        :param theme: an integer representing the theme of the level."""
        if theme == 0:
            non_solid = Animation([["assets/red_cross.png", "assets/blue_cross"]], position)
            non_solid.add(self.non_solids)
            non_solid.add(self.animations)

    def draw_objective(self, position, theme):
        """draw_objective() places an objective in the level.

        :param position: a tuple representing the spot to put the objective.
        :param theme: an integer representing the theme of the level."""
        objective = Tile("assets/coin.png", position)
        objective.add(self.objectives)

    def draw_filled(self, position):
        """draw_filled() renders a filled tile_set in the level.

        :param position: a tuple representing the spot to put the filled tile_set."""
        self.render_tileset(tile_sets.filled[0], position)

    def draw_walker_tileset(self, position, row, col):
        """draw_walker_tileset() renders an appropriate walker tile_set in the level.

        :param position: a tuple representing the spot to put the tile_set.
        :param row: an integer representing the row in the level of the location to check around.
        :param col: an integer representing the col in the level of the location to check around."""
        # State of coordinate
        above = False
        below = False
        right = False
        left = False

        tile_set = []

        # Checking above
        if self.level_layout[row - 1][col] != 'X' and self.level_layout[row - 1][col] != '0':
            above = True
        # Checking below
        if self.level_layout[row + 1][col] != 'X' and self.level_layout[row + 1][col] != '0':
            below = True
        # Checking right
        if self.level_layout[row][col + 1] != 'X' and self.level_layout[row][col + 1] != '0':
            right = True
        # Checking left
        if self.level_layout[row][col - 1] != 'X' and self.level_layout[row][col - 1] != '0':
            left = True

        # Choosing appropriate tileset
        if above and not below and not right and not left:
            tile_set = random.choice(tile_sets.e_up)

        elif below and not above and not left and not right:
            tile_set = random.choice(tile_sets.e_down)

        elif right and not left and not above and not below:
            tile_set = random.choice(tile_sets.e_right)

        elif left and not right and not below and not above:
            tile_set = random.choice(tile_sets.e_left)

        elif above and right and not left and not below:
            tile_set = random.choice(tile_sets.e_up_right)

        elif below and right and not above and not left:
            tile_set = random.choice(tile_sets.e_down_right)

        elif left and below and not right and not above:
            tile_set = random.choice(tile_sets.e_down_left)

        elif left and above and not right and not below:
            tile_set = random.choice(tile_sets.e_left_up)

        elif left and right and not above and not below:
            tile_set = random.choice(tile_sets.e_left_right)

        elif above and below and not left and not right:
            tile_set = random.choice(tile_sets.e_up_down)

        elif left and above and right and not below:
            tile_set = random.choice(tile_sets.e_right_up_left)

        elif above and below and right and not left:
            tile_set = random.choice(tile_sets.e_down_up_right)

        elif left and below and right and not above:
            tile_set = random.choice(tile_sets.e_down_right_left)

        elif above and left and below and not right:
            tile_set = random.choice(tile_sets.e_down_up_left)

        elif above and left and below and right:
            tile_set = random.choice(tile_sets.e_intersection)

        else:
            tile_set = random.choice(tile_sets.enclosed)

        self.render_tileset(tile_set, position)

    def draw_player_tileset(self, position, row, col):
        """draw_player_tileset() renders an appropriate player tile_set in the level.

        :param position: a tuple representing the spot to put the tile_set.
        :param row: an integer representing the row in the level of the location to check around.
        :param col: an integer representing the col in the level of the location to check around."""
        # State of coordinate
        above = False
        below = False
        right = False
        left = False

        tile_set = []

        # Checking above
        if self.level_layout[row - 1][col] != 'X' and self.level_layout[row - 1][col] != '0':
            above = True
        # Checking below
        if self.level_layout[row + 1][col] != 'X' and self.level_layout[row + 1][col] != '0':
            below = True
        # Checking right
        if self.level_layout[row][col + 1] != 'X' and self.level_layout[row][col + 1] != '0':
            right = True
        # Checking left
        if self.level_layout[row][col - 1] != 'X' and self.level_layout[row][col - 1] != '0':
            left = True

        # Choosing appropriate tileset
        if above and not below and not right and not left:
            tile_set = random.choice(tile_sets.p_up)

        elif below and not above and not left and not right:
            tile_set = random.choice(tile_sets.p_down)

        elif right and not left and not above and not below:
            tile_set = random.choice(tile_sets.p_right)

        elif left and not right and not below and not above:
            tile_set = random.choice(tile_sets.p_left)

        elif above and right and not left and not below:
            tile_set = random.choice(tile_sets.p_up_right)

        elif below and right and not above and not left:
            tile_set = random.choice(tile_sets.p_down_right)

        elif left and below and not right and not above:
            tile_set = random.choice(tile_sets.p_down_left)

        elif left and above and not right and not below:
            tile_set = random.choice(tile_sets.p_left_up)

        elif left and right and not above and not below:
            tile_set = random.choice(tile_sets.p_left_right)

        elif above and below and not left and not right:
            tile_set = random.choice(tile_sets.p_up_down)

        elif left and above and right and not below:
            tile_set = random.choice(tile_sets.p_right_up_left)

        elif above and below and right and not left:
            tile_set = random.choice(tile_sets.p_down_up_right)

        elif left and below and right and not above:
            tile_set = random.choice(tile_sets.p_down_right_left)

        elif above and left and below and not right:
            tile_set = random.choice(tile_sets.p_down_up_left)

        elif above and left and below and right:
            tile_set = random.choice(tile_sets.p_intersection)

        else:
            tile_set = random.choice(tile_sets.p_enclosed)

        self.render_tileset(tile_set, position)

    def draw_objective_tileset(self, position, row, col):
        """draw_objective_tileset() renders an appropriate objective tile_set in the level.

        :param position: a tuple representing the spot to put the tile_set.
        :param row: an integer representing the row in the level of the location to check around.
        :param col: an integer representing the col in the level of the location to check around."""
        # State of coordinate
        above = False
        below = False
        right = False
        left = False

        tile_set = []

        # Checking above
        if self.level_layout[row - 1][col] != 'X' and self.level_layout[row - 1][col] != '0':
            above = True
        # Checking below
        if self.level_layout[row + 1][col] != 'X' and self.level_layout[row + 1][col] != '0':
            below = True
        # Checking right
        if self.level_layout[row][col + 1] != 'X' and self.level_layout[row][col + 1] != '0':
            right = True
        # Checking left
        if self.level_layout[row][col - 1] != 'X' and self.level_layout[row][col - 1] != '0':
            left = True

        # Choosing appropriate tileset
        if above and not below and not right and not left:
            tile_set = random.choice(tile_sets.o_up)

        elif below and not above and not left and not right:
            tile_set = random.choice(tile_sets.o_down)

        elif right and not left and not above and not below:
            tile_set = random.choice(tile_sets.o_right)

        elif left and not right and not below and not above:
            tile_set = random.choice(tile_sets.o_left)

        elif above and right and not left and not below:
            tile_set = random.choice(tile_sets.o_up_right)

        elif below and right and not above and not left:
            tile_set = random.choice(tile_sets.o_down_right)

        elif left and below and not right and not above:
            tile_set = random.choice(tile_sets.o_down_left)

        elif left and above and not right and not below:
            tile_set = random.choice(tile_sets.o_left_up)

        elif left and right and not above and not below:
            tile_set = random.choice(tile_sets.o_left_right)

        elif above and below and not left and not right:
            tile_set = random.choice(tile_sets.o_up_down)

        elif left and above and right and not below:
            tile_set = random.choice(tile_sets.o_right_up_left)

        elif above and below and right and not left:
            tile_set = random.choice(tile_sets.o_down_up_right)

        elif left and below and right and not above:
            tile_set = random.choice(tile_sets.o_down_right_left)

        elif above and left and below and not right:
            tile_set = random.choice(tile_sets.o_down_up_left)

        elif above and left and below and right:
            tile_set = random.choice(tile_sets.o_intersection)

        else:
            tile_set = random.choice(tile_sets.enclosed)

        self.render_tileset(tile_set, position)

    def draw_flier_tileset(self, position, row, col):
        """draw_flier_tileset() renders an appropriate flier tile_set in the level.

        :param position: a tuple representing the spot to put the tile_set.
        :param row: an integer representing the row in the level of the location to check around.
        :param col: an integer representing the col in the level of the location to check around."""
        # State of coordinate
        above = False
        below = False
        right = False
        left = False

        tile_set = []

        # Checking above
        if self.level_layout[row - 1][col] != 'X' and self.level_layout[row - 1][col] != '0':
            above = True
        # Checking below
        if self.level_layout[row + 1][col] != 'X' and self.level_layout[row + 1][col] != '0':
            below = True
        # Checking right
        if self.level_layout[row][col + 1] != 'X' and self.level_layout[row][col + 1] != '0':
            right = True
        # Checking left
        if self.level_layout[row][col - 1] != 'X' and self.level_layout[row][col - 1] != '0':
                left = True

        if above and not below and not right and not left:
            tile_set = random.choice(tile_sets.f_up)

        elif below and not above and not left and not right:
            tile_set = random.choice(tile_sets.f_down)

        elif right and not left and not above and not below:
            tile_set = random.choice(tile_sets.f_right)

        elif left and not right and not below and not above:
            tile_set = random.choice(tile_sets.f_left)

        elif above and right and not left and not below:
            tile_set = random.choice(tile_sets.f_up_right)

        elif below and right and not above and not left:
            tile_set = random.choice(tile_sets.f_down_right)

        elif left and below and not right and not above:
            tile_set = random.choice(tile_sets.f_down_left)

        elif left and above and not right and not below:
            tile_set = random.choice(tile_sets.f_left_up)

        elif left and right and not above and not below:
            tile_set = random.choice(tile_sets.f_left_right)

        elif above and below and not left and not right:
            tile_set = random.choice(tile_sets.f_up_down)

        elif left and above and right and not below:
            tile_set = random.choice(tile_sets.f_right_up_left)

        elif above and below and right and not left:
            tile_set = random.choice(tile_sets.f_down_up_right)

        elif left and below and right and not above:
            tile_set = random.choice(tile_sets.f_down_right_left)

        elif above and left and below and not right:
            tile_set = random.choice(tile_sets.f_down_up_left)

        elif above and left and below and right:
            tile_set = random.choice(tile_sets.f_intersection)

        else:
            tile_set = random.choice(tile_sets.enclosed)

        self.render_tileset(tile_set, position)

    # draws a tileset of blocks
    def draw_tileset(self, position, row, col):
        """draw_tileset() renders an appropriate path non-entity tile_set in the level.

        :param position: a tuple representing the spot to put the tile_set.
        :param row: an integer representing the row in the level of the location to check around.
        :param col: an integer representing the col in the level of the location to check around."""
        # State of coordinate
        above = False
        below = False
        right = False
        left = False

        tile_set = []

        # Checking above
        if self.level_layout[row - 1][col] != 'X' and self.level_layout[row - 1][col] != '0':
            above = True
        # Checking below
        if self.level_layout[row + 1][col] != 'X' and self.level_layout[row + 1][col] != '0':
            below = True
        # Checking right
        if self.level_layout[row][col + 1] != 'X' and self.level_layout[row][col + 1] != '0':
            right = True
        # Checking left
        if self.level_layout[row][col - 1] != 'X' and self.level_layout[row][col - 1] != '0':
            left = True

        if above and not below and not right and not left:
            tile_set = random.choice(tile_sets.up)

        elif below and not above and not left and not right:
            tile_set = random.choice(tile_sets.down)

        elif right and not left and not above and not below:
            tile_set = random.choice(tile_sets.right)

        elif left and not right and not below and not above:
            tile_set = random.choice(tile_sets.left)

        elif above and right and not left and not below:
            tile_set = random.choice(tile_sets.up_right)

        elif below and right and not above and not left:
            tile_set = random.choice(tile_sets.down_right)

        elif left and below and not right and not above:
            tile_set = random.choice(tile_sets.down_left)

        elif left and above and not right and not below:
            tile_set = random.choice(tile_sets.left_up)

        elif left and right and not above and not below:
            tile_set = random.choice(tile_sets.left_right)

        elif above and below and not left and not right:
            tile_set = random.choice(tile_sets.up_down)

        elif left and above and right and not below:
            tile_set = random.choice(tile_sets.right_up_left)

        elif above and below and right and not left:
            tile_set = random.choice(tile_sets.down_up_right)

        elif left and below and right and not above:
            tile_set = random.choice(tile_sets.down_right_left)

        elif above and left and below and not right:
            tile_set = random.choice(tile_sets.down_up_left)

        elif above and left and below and right:
            tile_set = random.choice(tile_sets.intersection)

        else:
            tile_set = random.choice(tile_sets.enclosed)

        self.render_tileset(tile_set, position)

    def render_tileset(self, tileset, position):
        """render_tileset() places all the objects in a tile_set into the level.

        :param tileset: a list of strings representing the tile_set.
        :param position: a tuple representing the place to render the top left of the tile_set."""
        for row in range(0, len(tileset)):
            for col in range(0, len(tileset[row])):

                # Position refers to the place that the levelrenderer points to,
                # subposition points to a place within that position.
                subposition = (position[0] +(col * self.tile_size), position[1] + (row * self.tile_size))

                # Add cases here for different types of tiles in a tileset.
                if tileset[row][col] == 'P':
                    self.draw_player(subposition, settings.curr_difficulty) # Making darkness a function of difficulty

                elif tileset[row][col] == 'E':
                    self.draw_walker(subposition, self.theme)

                elif tileset[row][col] == 'F':
                    self.draw_flier(subposition, self.theme)

                elif tileset[row][col] == 'B':
                    self.draw_background(self.theme)

                elif tileset[row][col] == 'X':
                    self.draw_block(subposition, self.theme)

                elif tileset[row][col] == 'Y':
                    self.draw_block_animation(subposition, self.theme)

                elif tileset[row][col] == 'N':
                    self.draw_non_solid(subposition, self.theme)

                elif tileset[row][col] == 'A':
                    self.draw_non_solid_animation(subposition, self.theme)

                elif tileset[row][col] == 'O':
                    self.draw_objective(subposition, self.theme)

    def fill(self, position, h_asset_size, v_asset_size, h_space_size, v_space_size, selector, sprite_set):
        """fill(): This may be useful for resolving asset size conflicts, but I do not know if it will be needed.
        This function takes a lot of arguments, and should ideally be called from a draw handler.
        This function fills a space specified as h_space_size by v_space_size, with the top left
        of this area located at position, with the constructed object, determined by selector, with the given
        sprite_set, if applicable.
        h_space_size should be evenly divisible by h_asset_size, and v_space_size should be evenly divisible
        by v_asset_size
        This function can create a lot of sprite objects very quickly, please use it sparingly.

        :param position: a tuple representing the top left of the place to fill.
        :param h_asset_size: an integer of the horizontal size of the asset to fill.
        :param v_asset_size: an integer of the vertical size of the asset to fill.
        :param h_space_size: an integer of the horizontal size of the space to fill. Must be evenly divisible by
        h_asset_size.
        :param v_space_size: an integer of the vertical size of the space to fill. Must be evenly divisible by
        v_asset_size.
        :param selector: a string determining what constructors are used for the assets.
        :param sprite_set: a string, or list of lists of strings if you are filling an animation,
         representing the filepath(s) to the images of the assets.
         :returns: a list of the sprite objects that were placed."""
        assets = []
        h_counter = 0

        if selector == "Walker":
            while h_counter < h_space_size:
                v_counter = 0
                while v_counter < v_space_size:
                    enemy = Walker((position[0] + h_counter, position[1] + v_counter))
                    assets.append(enemy)
                    v_counter += v_asset_size
                h_counter += h_asset_size

        elif selector == "Flyer":
            while h_counter < h_space_size:
                v_counter = 0
                while v_counter < v_space_size:
                    enemy = Flier((position[0] + h_counter, position[1] + v_counter))
                    assets.append(enemy)
                    v_counter += v_asset_size
                h_counter += h_asset_size

        elif selector == "Tile":
            while h_counter < h_space_size:
                v_counter = 0
                while v_counter < v_space_size:
                    block = Tile(sprite_set, (position[0] + h_counter, position[1] + v_counter))
                    assets.append(block)
                    v_counter += v_asset_size
                h_counter += h_asset_size

        elif selector == "Animation":
            while h_counter < h_space_size:
                v_counter = 0
                while v_counter < v_space_size:
                    animation = Animation(sprite_set, (position[0] + h_counter, position[1] + v_counter))
                    assets.append(animation)
                    v_counter += v_asset_size
                h_counter += h_asset_size

        return assets
