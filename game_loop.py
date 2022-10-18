import pygame
from settings import *
from tile import *
from player import *
from level_renderer import *

pygame.init()

run = True
screen = pygame.display.set_mode((screen_width, screen_height))

frame_limiter = pygame.time.Clock()
test_level = LevelRenderer(screen, settings.level0)
keys_pressed = []
player = test_level.get_player()
testenemy = test_level.get_enemies().sprites()[0]

SPRITE_NEXT = pygame.USEREVENT + 1

pygame.time.set_timer(SPRITE_NEXT, 100, 0)
while run:
    # Pygame event handling.
    events = pygame.event.get()
    for next_event in events:
        if next_event.type == pygame.QUIT:
            run = False
        if next_event.type == SPRITE_NEXT:
            for sprite in test_level.get_animations().sprites():
                sprite.next(0)

    #x_e_mov = testenemy.move_int
    if testenemy.edge_detect(test_level.solids) == True:   # Supposed to reverse movement direction if edge_detect == True
        testenemy.move_int = testenemy.move_int * -1
    testenemy.move_x(testenemy.move_int,test_level.solids)

    player_init_pos = (player.rect.x, player.rect.y) # Grabbing the initial position of the player in the frame.
    keys_pressed = pygame.key.get_pressed()  # Array of bools accessed with the pygame key constants.
    # Uses the fact that true is one and false is 0 to evaluate the direction to move.
    # Neatly handles contradictory input cases.
    x_mov = keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]
    y_mov = keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]

    player.move_x(x_mov,test_level.solids)
    if y_mov == -1 and player.touching_ground(test_level.solids): # -1 is up for y
        player.boing = player.jump_power
    player.jump(test_level.solids)
    player.fall(test_level.solids)
    player_fin_pos = (player.rect.x, player.rect.y) # Grabbing the final position of the player in the frame.
    test_level.update(player_init_pos,player_fin_pos) # The level_renderer can go draw everything.
    frame_limiter.tick(max_frames) # Capping the frames for consistent behaviour.
    pygame.display.update()

pygame.display.quit()