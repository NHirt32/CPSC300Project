import pygame

import level_generator
from settings import *
from tile import *
from player import *
from level_renderer import *
import random
pygame.init()

gameOver = False; #Going to use this for encasing game in loop, when player touches enemy/hazard it is set to True
#enemy_group = pygame.sprite.Group() #Group of sprites used to hold multiple enemies
run = True
screen = pygame.display.set_mode((screen_width, screen_height))

frame_limiter = pygame.time.Clock()

# For testing purposes, hard coded theme, and tile_size
test_level = LevelRenderer(screen, settings.levelM, 1)
keys_pressed = []
player = test_level.get_player()
#testenemy = test_level.get_enemies().sprites()[0]
#testenemy1 = test_level.get_enemies().sprites()[1]

SPRITE_NEXT = pygame.USEREVENT + 1

pygame.time.set_timer(SPRITE_NEXT, 70, 0)
while run:
    # Pygame event handling.
    events = pygame.event.get()
    for next_event in events:
        if next_event.type == pygame.QUIT:
            run = False
        if next_event.type == SPRITE_NEXT:
            for sprite in test_level.get_animations().sprites():
                sprite.next(sprite.direction)

    keys_pressed = pygame.key.get_pressed()  # Array of bools accessed with the pygame key constants.
    # Uses the fact that true is one and false is 0 to evaluate the direction to move.
    # Neatly handles contradictory input cases.
    x_mov = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]
    y_mov = keys_pressed[pygame.K_s] - keys_pressed[pygame.K_SPACE]

    for enemy in test_level.get_enemies().sprites():  # Initializes all enemies, currently turning around is broken
        if (enemy.edge_detect(test_level.solids) == False): # If the enemy is not colliding with a solid
            enemy.move_x(enemy.move_int, test_level.solids)
        else:   #If the enemy is colliding with a solid
            enemy.move_int *= -1    # Turn around
            enemy.move_x(enemy.move_int, test_level.solids) # Move slightly to avoid being stuck on the wall

    player_init_pos = (player.rect.x, player.rect.y)  # Grabbing the initial position of the player in the frame.
    player.update(x_mov, y_mov, test_level.solids) # Player Movement Processed
    player_fin_pos = (player.rect.x, player.rect.y) # Grabbing the final position of the player in the frame.

    if player.collided_with(test_level.enemies):    # If the player collides with an enemy
        gameOver = True
        test_level = LevelRenderer(screen, settings.levelM, 1)  # Reload the level
        player = test_level.get_player()    # Reload the player

    test_level.update(player_init_pos,player_fin_pos) # The level_renderer can go draw everything.
    frame_limiter.tick(max_frames) # Capping the frames for consistent behaviour.
    pygame.display.update()

pygame.display.quit()

# def level_init(){
#     player = test_level.get_player()
#
# }