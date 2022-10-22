import pygame
import settings
from settings import *
from tile import *
from player import *
from animation import *
from enemy import *


class LevelRenderer:

    def __init__(self, screen, level_layout):
        self.animations = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.backgrounds = pygame.sprite.Group()
        self.screen = screen
        self.level_layout = level_layout
        self.background_speed = 0.1

        # Add any further sprite groups that need camera offset into this array.
        # The order of drawing is from left to right.
        self.all_tiles = [self.backgrounds, self.solids, self.enemies, self.players]

        # Drawing the layout to the screen
        for row in range(0, len(level_layout)):
            for col in range(0, len(level_layout[row])):

                position = ((col * settings.tile_size), (row * settings.tile_size))

                # Add cases here for different tiles.
                if level_layout[row][col] == "P":
                    player1 = Player(position)
                    player1.add(self.players)   #Adds player1 to renderer group
                    player1.add(self.animations)

                elif level_layout[row][col] == 'E':
                    enemy1 = Enemy(position)
                    enemy1.add(self.enemies)
                    #enemy1.add(self.solids)


                elif level_layout[row][col] == "T":

                    outline_top = Tile("assets/outline_top.png", position)
                    outline_top.add(self.solids)

                elif level_layout[row][col] == "L":
                    r_outline_left = Tile("assets/r_outline_left.png", position)
                    r_outline_left.add(self.solids)

                elif level_layout[row][col] == "C":
                    outcorner_topleft = Tile("assets/outcorner_topleft.png", position)
                    outcorner_topleft.add(self.solids)

                elif level_layout[row][col] == "H":
                    corner_topright = Tile("assets/corner_topright.png", position)
                    corner_topright.add(self.solids)

                elif level_layout[row][col] == "R":
                    line_right = Tile("assets/line_right.png", position)
                    line_right.add(self.solids)

                elif level_layout[row][col] == "B":
                    large_80_40_background = Tile("assets/large_80_40_background.png", position)
                    large_80_40_background.add(self.backgrounds)

                elif level_layout[row][col] == "X":
                    paper_block = Tile("assets/paper_block.png", position)
                    paper_block.add(self.solids)

                elif level_layout[row][col] == "A":
                    animation_test = Animation(
                        [["assets/red_cross.png", "assets/blue_cross.png"], ["assets/birds.png"]], position)
                    animation_test.add(self.solids)
                    animation_test.add(self.animations)

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
        # perhaps make it move at 1/2 the rate of everything else for a perceived depth.

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

        self.screen.fill("white")  # This is a temporary background.

        # Drawing all sprites in the group to screen.
        self.backgrounds.draw(self.screen)
        self.solids.draw(self.screen)
        self.enemies.draw(self.screen)
        self.players.draw(self.screen)

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
