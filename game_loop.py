import pygame
import game_menu
import settings
from settings import *
from tile import *
from player import *
from level_renderer import *
import random

# Moves the camera
def update_camera():
    size = screen.get_size()
    screen_width = size[0]
    screen_height = size[1]
    init = (player.rect.x, player.rect.y)  # Grabbing the initial position of the player in the frame.
    test_level.update((screen_width / 2, screen_height / 2), init)

game_menu.main()
pygame.init()

gameOver = False;  # Going to use this for encasing game in loop, when player touches enemy/hazard it is set to True
run = True
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
frame_limiter = pygame.time.Clock()
test_level = LevelRenderer(screen, settings.levelM, settings.theme)
keys_pressed = []
player = test_level.get_player()
completed = False
SPRITE_NEXT = pygame.USEREVENT + 1
screen_flag = False
joystick = 0
j_offset = 0.2  # corresponds to how touchy the controller is.
pygame.time.set_timer(SPRITE_NEXT, 70, 0)

while run:
    # Pygame event handling.
    events = pygame.event.get()
    for next_event in events:
        if next_event.type == pygame.QUIT:
            run = False
        if (next_event.type == pygame.JOYDEVICEADDED) and (joystick == 0):
            # If new controller is added
            joystick = pygame.joystick.Joystick(0)
        if next_event.type == pygame.JOYDEVICEREMOVED:
            # If controller is removed
            joystick = 0
        if next_event.type == SPRITE_NEXT:
            for sprite in test_level.get_animations().sprites():
                sprite.next()
        if next_event.type == pygame.WINDOWSIZECHANGED:
            # Update screen size, move camera accordingly
            update_camera()

    # Clearing input from the last frame
    right_jmov = False
    left_jmov = False
    up_jmov = False
    down_jmov = False

    if joystick != 0:
        x_state = joystick.get_axis(0)
        y_state = joystick.get_axis(1)
        up_jmov = joystick.get_button(0)

        if x_state > j_offset:
            right_jmov = True
            left_jmov = False
        elif x_state < -j_offset:
            right_jmov = False
            left_jmov = True
        else:
            right_jmov = False
            left_jmov = False

        if y_state < -j_offset:
            down_jmov = False
        elif y_state > j_offset:
            down_jmov = True

    keys_pressed = pygame.key.get_pressed()  # Array of bools accessed with the pygame key constants.
    # Uses the fact that true is one and false is 0 to evaluate the direction to move.
    # Neatly handles contradictory input cases.
    x_mov = (keys_pressed[pygame.K_d] or right_jmov) - (keys_pressed[pygame.K_a] or left_jmov)
    y_mov = (keys_pressed[pygame.K_s] or down_jmov) - (keys_pressed[pygame.K_SPACE] or up_jmov)

    if keys_pressed[pygame.K_F11]:
        screen_flag = not screen_flag

        if screen_flag:
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
            update_camera()
        else:
            # NEEDS TO BE DONE TWICE, THIS IS A PROBLEM WITH PYGAME.
            # More information at https://github.com/pygame/pygame/issues/3107
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # Check to see if the player collided in the last frame
    if player.collided_with(test_level.enemies) and not completed:  # If the player collides with an enemy
        gameOver = True
        test_level = LevelRenderer(screen, settings.levelM, settings.theme)  # Reload the level
        player = test_level.get_player()  # Reload the player

    player_init_pos = (player.rect.x, player.rect.y)  # Grabbing the initial position of the player in the frame.
    player.update(x_mov, y_mov, test_level.solids)  # Player Movement Processed
    player_fin_pos = (player.rect.x, player.rect.y)  # Grabbing the final position of the player in the frame.

    for enemy in test_level.get_enemies().sprites():  # Initializes all enemies
        enemy.update(test_level.solids)  # Move the enemy

        # If the enemy was killed
        if enemy.died(player):
            test_level.enemies.remove([enemy])
            player.vertical_momentum = 10  # make the player jump up a little.

    # If player collided with objective
    for objective in test_level.objectives.sprites():
        if objective.rect.colliderect(player.rect):
            test_level.objectives.remove([objective])  # Not sure if works.

    # If got all objectives
    if (len(test_level.objectives.sprites()) == 0):
        completed = True

    test_level.update(player_init_pos, player_fin_pos)  # The level_renderer can go draw everything.
    frame_limiter.tick(max_frames)  # Capping the frames for consistent behaviour.
    pygame.display.update()

pygame.display.quit()





