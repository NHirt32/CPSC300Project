"""game_loop is the driver program of the game, everything is run from game_loop. It is most of the classes interact,
and so small changes in game_loop can have large impacts to the features in the game."""

import game_menu
import pause_menu
from settings import *
from level_renderer import *
import time
import json

def update_camera():
    """update_camera() re-centers the camera over the player, when a new level is loaded or an attribute
    about the screen changes."""
    size = screen.get_size()
    screen_width = size[0]
    screen_height = size[1]
    init = (player.rect.x, player.rect.y)  # Grabbing the initial position of the player in the frame.
    test_level.update((screen_width / 2, screen_height / 2), init)


def deathScreen():
    """deathScreen() draws the death-screen onto the screen when it is called, and waits a small amount of time."""
    font = pygame.font.Font("assets/OptimusPrinceps.ttf", 56)
    text = font.render("YOU DIED", True, (139, 0, 0), (0, 0, 0))

    textRect = text.get_rect()
    textRect.center = (settings.screen_width // 2, settings.screen_height // 2)

    screen.fill((0, 0, 0))
    screen.blit(text, textRect)
    pygame.display.update()

    time.sleep(0.75)


def winScreen():
    """winScreen() draws the win-screen to the screen. This involves calculating the final score and may involve
    saving it to the scores file as well."""
    settings.end_time = time.time()
    settings.score -= ((int(settings.end_time - settings.start_time)) * (settings.curr_difficulty * 10))

    font = pygame.font.Font("assets/OptimusPrinceps.ttf", 56)
    text = font.render("YOU WIN ! ", True, (255, 170, 29), (0, 0, 0))
    text2 = font.render(("Score: " + str(settings.score)), True, (255, 170, 29), (0, 0, 0))

    textRect = text.get_rect()
    textRect.center = (settings.screen_width // 2, settings.screen_height // 2)

    textRect2 = text.get_rect()
    textRect2.center = (settings.screen_width // 2, (settings.screen_height // 2) + 75)

    screen.fill((0, 0, 0))
    screen.blit(text, textRect)
    screen.blit(text2, textRect2)

    pygame.display.update()

    with open("scores.json", 'r+') as jsonFile:
        data = json.load(jsonFile)
        str1 = str(settings.curr_difficulty) + "-"
        str1 += str(settings.curr_level)
        if settings.score > data[str1]:
            data[str1] = settings.score
            jsonFile.seek(0)
            json.dump(data, jsonFile, indent=4)
            jsonFile.truncate()

    time.sleep(2.0)

# Program start

pygame.init()

run = True

pygame.init()

# Animation next events
PLAYER_SPRITE_NEXT = pygame.USEREVENT + 1
FLAME_SPRITE_NEXT = pygame.USEREVENT + 2
SPRITE_NEXT = pygame.USEREVENT + 3

# Setting allowed events lessens the load a little on frames.
pygame.event.set_allowed([PLAYER_SPRITE_NEXT, FLAME_SPRITE_NEXT, SPRITE_NEXT, pygame.JOYDEVICEADDED,
                          pygame.JOYDEVICEREMOVED, pygame.QUIT, pygame.WINDOWSIZECHANGED])

while run:
    settings.curr_level = -1
    settings.score = 10000

    game_menu.main()

    if settings.curr_level == -1:
        break

    gameOver = False  # Going to use this for encasing game in loop, when player touches enemy/hazard it is set to True.
    in_game = True

    # the pygame.DOUBLEBUF flag helps our frames a bit.
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
    frame_limiter = pygame.time.Clock()

    test_level = LevelRenderer(screen, settings.levelM, settings.curr_level)
    keys_pressed = []
    player = test_level.players.sprites()[0]
    completed = False

    screen_flag = False

    joystick = 0
    if pygame.joystick.get_count() != 0:
        joystick = pygame.joystick.Joystick(0)

    j_offset = 0.2  # Corresponds to how touchy the controller is.

    # Animation Timers
    pygame.time.set_timer(PLAYER_SPRITE_NEXT, 200, 0)
    pygame.time.set_timer(FLAME_SPRITE_NEXT, 200, 0)
    pygame.time.set_timer(SPRITE_NEXT, 100, 0)
    font = pygame.font.Font("assets/OptimusPrinceps.ttf", 26)

    settings.start_time = time.time()
    while in_game:

        # Pygame event handling
        events = pygame.event.get()
        for next_event in events:
            if next_event.type == pygame.QUIT:
                in_game = False
                run = False
            if (next_event.type == pygame.JOYDEVICEADDED) and (joystick == 0):
                # If new controller is added.
                joystick = pygame.joystick.Joystick(0)
            if next_event.type == pygame.JOYDEVICEREMOVED:
                # If controller is removed.
                joystick = 0
            if next_event.type == PLAYER_SPRITE_NEXT:
                player.next()
            if next_event.type == FLAME_SPRITE_NEXT:
                test_level.effects.sprites()[0].next()
            if next_event.type == SPRITE_NEXT:
                # Only update the animation if near player, in the dark.
                for animation in test_level.animations.sprites():
                    if animation.rect.colliderect(test_level.effects.sprites()[1].rect):
                        animation.next()
            if next_event.type == pygame.WINDOWSIZECHANGED:
                # Update screen size, move camera accordingly.
                update_camera()

        # Clearing input from the last frame.
        right_jmov = False
        left_jmov = False
        up_jmov = False
        down_jmov = False

        # Handling controller input.
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

        # Pause case
        if keys_pressed[pygame.K_p] or keys_pressed[pygame.K_ESCAPE]:
            pause_menu.main()

            if settings.pause_status == 0:
                gameOver = True
                test_level = LevelRenderer(screen, settings.levelM, settings.curr_level)  # Reload the level.
                player = test_level.players.sprites()[0]  # Reload the player.
                update_camera()

            elif settings.pause_status == 1:
                settings.start_time = time.time()
                settings.score = 10000
                in_game = False

            elif settings.pause_status == 2:
                in_game = False
                run = False

            elif settings.pause_status == 3:
                continue

        player_init_pos = (player.rect.x, player.rect.y)  # Grabbing the initial position of the player in the frame.
        player.update(x_mov, y_mov, test_level.p_solids)  # Player Movement Processed.
        player_fin_pos = (player.rect.x, player.rect.y)  # Grabbing the final position of the player in the frame.

        # Update Phil's flame, slight offset for looks.
        test_level.effects.sprites()[0].rect.midbottom = (player.rect.midtop[0] - 1, player.rect.midtop[1])
        # Update the dark.
        test_level.effects.sprites()[1].rect.center = player.rect.center

        for enemy in test_level.enemies.sprites():  # Initializes all enemies.
            # Only update them if they are in the dark around the player.
            if (enemy.rect.colliderect(test_level.effects.sprites()[1].rect)):
                enemy.update(test_level.e_solids)  # Move the enemy.

                # If the enemy was killed.
                if enemy.died(test_level.players):
                    settings.score += settings.kill_reward
                    enemy.kill()
                    player.vertical_momentum = 10  # Make the player jump up a little.

        # Check to see if the player is touching an enemy.
        if player.touching_right(test_level.enemies) or player.touching_left(test_level.enemies) or \
            player.touching_roof(test_level.enemies) and not completed:  # If the player collides with an enemy

            if time.time() - player.last_hurt >= 0.45 or player.last_hurt == 0:

                rounded = min(255, max(0, round(255 * 0.40)))
                screen.fill((255, rounded, rounded), special_flags=pygame.BLEND_MULT)
                pygame.display.update()
                settings.score -= settings.hurt_penalty
                time.sleep(0.15)

                player.last_hurt = time.time()

                # If the player died.
                player.health -= 1
                if player.health == 0:
                    gameOver = True
                    settings.score -= settings.death_penalty
                    deathScreen()
                    test_level = LevelRenderer(screen, settings.levelM, settings.curr_level)  # Reload the level
                    player = test_level.players.sprites()[0]  # Reload the player
                    update_camera()

        # If player collided with objective.
        for objective in test_level.objectives.sprites():
            if objective.rect.colliderect(player.rect):
                objective.kill()

        # If got all objectives.
        if (len(test_level.objectives.sprites()) == 0):
            winScreen()
            completed = True
            in_game = False

        # Handles drawing everything to the screen after updates, also handles moving the camera in a level.
        test_level.update(player_init_pos, player_fin_pos)

        frame_limiter.tick(max_frames)  # Capping the frames for consistent behaviour.

        # Drawing the remaining coins.
        text = font.render("COINS:   " + str(len(test_level.objectives.sprites())) + "   ", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (settings.screen_width - 80, 25)
        screen.blit(text, textRect)

        # Drawing the remaining health.
        text = font.render("   HEALTH:   " + str(player.health) + "   ", True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (settings.screen_width - 80, 50)
        screen.blit(text, textRect)

        pygame.display.update()

    pygame.display.quit()
