import pygame
import settings
from settings import *
from tile import *
from player import *
from animation import *
from walker import *
from flier import *
import random

class LevelRenderer:

    def __init__(self, screen, level_layout, theme):
        self.animations = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.non_solids = pygame.sprite.Group()
        self.objectives = pygame.sprite.Group()
        self.effects = pygame.sprite.Group()
        self.screen = screen
        self.level_layout = level_layout
        self.background_speed = 0.1
        self.theme = theme

        # Remember, a chosen tile_size should be evenly divisible by all assets that
        # are drawn using the fill() function in level renderer
        if theme == 0:
            tile_sizes = [128,192,256]
            self.tile_size = random.choice(tile_sizes)

        elif theme == 1:
            tile_sizes = [192]
            self.tile_size = random.choice(tile_sizes)

        # Add any further sprite groups that need camera offset into this array.
        # The order of drawing is from left to right.
        self.all_tiles = [self.backgrounds, self.solids, self.non_solids, self.objectives, self.enemies, self.players,
                          self.effects]

        # Drawing the layout to the screen
        for row in range(0, len(level_layout)):
            for col in range(0, len(level_layout[row])):

                position = ((col * self.tile_size), (row * self.tile_size))

                # Add cases here for different types of tiles.
                if level_layout[row][col] == 'P':
                    self.draw_player(position,self.theme)

                elif level_layout[row][col] == 'E':
                    self.draw_walker(position, self.theme)

                elif level_layout[row][col] == 'F':
                    self.draw_flier(position, self.theme)

                elif level_layout[row][col] == 'B':
                    self.draw_background(position, self.theme)

                elif level_layout[row][col] == 'X':
                    self.draw_block(position, self.theme)

                elif level_layout[row][col] == 'Y':
                    self.draw_block_animation(position, self.theme)

                elif level_layout[row][col] == 'N':
                    self.draw_non_solid(position, self.theme)

                elif level_layout[row][col] == 'A':
                    self.draw_non_solid_animation(position, self.theme)

                elif level_layout[row][col] == 'O':
                    self.draw_objective(position, self.theme)

        # Need to move the camera over the player at the start, otherwise there may be an awkward offset
        init = (self.players.sprites()[0].rect.x, self.players.sprites()[0].rect.y)

        # The offset is reversed with its tuples, can simply use update to draw them
        self.update((settings.screen_width / 2, settings.screen_height / 2), init)

    # Draws everything to the screen with appropriate offset.
    def update(self, init_pos, final_pos):
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
        player1 = Player(position)
        player1.add(self.players)  # Adds player1 to renderer group
        player1.add(self.animations)
        flame = \
            Animation([["assets/flame1_1.png", "assets/flame1_2.png", "assets/flame1_1.png", "assets/flame1_3.png"]],
                      position)
        flame.add(self.effects)
        flame.add(self.animations)

    def draw_walker(self, position, theme):
        enemy1 = Walker(position)
        enemy1.add(self.enemies)
        #enemy1.add(self.solids)

    def draw_flier(self, position, theme):
        enemy1 = Flier(position)
        enemy1.add(self.enemies)
        #enemy1.add(self.solids)

    def draw_block(self, position, theme):
        if theme == 0:
            asset_size = 64
            blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile", "assets/paper_block.png")
            for block in blocks:
                block.add(self.solids)

        elif theme == 1:
            asset_size = 192
            blocks = self.fill(position, asset_size, asset_size, self.tile_size, self.tile_size, "Tile", "assets/test.png")
            for block in blocks:
                block.add(self.solids)

    def draw_block_animation(self, position, theme):
        if theme == 0:
            block = Animation([["assets/green_block.png", "assets/red_block.png"]], position)
            block.add(self.solids)
            block.add(self.animations)

    def draw_background(self, position, theme):
        if theme == 0:
            background = Tile("assets/large_80_40_background.png",position)
            background.add(self.backgrounds)

    def draw_non_solid(self, position, theme):
        if theme == 0:
            non_solid = Tile("assets/red_cross.png", position)
            non_solid.add(self.non_solids)

    def draw_non_solid_animation(self, position, theme):
        if theme == 0:
            non_solid = Animation([["assets/red_cross.png", "assets/blue_cross"]], position)
            non_solid.add(self.non_solids)
            non_solid.add(self.animations)

    def draw_objective(self, position, theme):
        objective = Tile("assets/red_cross.png", position)
        objective.add(self.objectives)

    def set_players(self, players):
        self.players = players

    def set_solids(self, solids):
        self.solids = solids

    def set_enemies(self, enemies):
        self.enemies = enemies

    def set_screen(self, screen):
        self.screen = screen

    def set_level_layout(self, level_layout):
        self.level_layout = level_layout

    def set_background_speed(self, background_speed):
        self.background_speed = background_speed

    def set_animations(self, animations):
        self.animations = animations

    # returns the players group
    def get_players(self):
        return self.players

    def get_solids(self):
        return self.solids

    def get_enemies(self):
        return self.enemies

    def get_screen(self):
        return self.screen

    def get_level_layout(self):
        return self.level_layout

    def get_background_speed(self):
        return self.background_speed

    # returns the first player sprite in players group
    def get_player(self):
        return self.players.sprites()[0]

    # returns a group of the animations
    def get_animations(self):
        return self.animations

    # This may be useful for resolving asset size conflicts, but I do not know if it will be needed.
    # This function takes a lot of arguments, and should ideally be called from a draw handler.
    # May have bugs. This function fills a space specified as h_space_size by v_space_size, with the top left
    # of this area located at position, with the constructed object, determined by selector, with the given
    # sprite_set, if applicable.
    # h_space_size should be evenly divisible by h_asset_size, and v_space_size should be evenly divisible
    # by v_asset_size
    # This function can create a lot of sprite objects very quickly, please use it sparingly.
    def fill(self, position, h_asset_size, v_asset_size, h_space_size, v_space_size, selector, sprite_set):
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
