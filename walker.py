import pygame
import enemy #Inherits functionality from enemy

class Walker(enemy.Enemy):

    def __init__(self, pos):
        enemy.Enemy.__init__(self, [["assets/red_player.png"]], pos)
        self.gravity = -100  # Defines max fall speed, MUST BE NEGATIVE
        self.vertical_momentum = 0
        self.ledge_offset = 0

    # Does mostly downward vertical movement, but needs to factor in when sliding and when not sliding.
    def gravity_handler(self, group):
        # if falling
        if (not self.touching_ground(group)):
            if self.vertical_momentum <= 0:
                self.v_move_y(1, abs(self.vertical_momentum), group)
                if (self.vertical_momentum < self.gravity):
                    self.vertical_momentum += 1
                else:
                    self.vertical_momentum -= 1

    # Processes all movement for the walker
    def update(self, group):

        if not self.touching_ground(group):
            1

        elif self.edge_detect(group):
            self.move_int *= -1
            self.move_x(self.move_int, group) # Move slightly to avoid being stuck on the wall

        #If the enemy is moving left and a ledge on left
        elif (self.move_int == -1) and self.ledge_left(group):
            self.move_int = 1  # Turn around
            self.move_x(self.move_int, group)  # Move slightly to avoid being stuck on the wall

        # If the enemy is moving right and a ledge on right
        elif (self.move_int == 1) and self.ledge_right(group):
            self.move_int = -1  # Turn around
            self.move_x(self.move_int, group)  # Move slightly to avoid being stuck on the wall

        else:
            self.move_x(self.move_int, group)

        # Primitive enemy gravity handling.
        self.gravity_handler(group)

    # Returns true if a ledge is on left of walker
    def ledge_left(self, group):
        # Just below and left of enemy.
        test_point = ((self.rect.bottomleft[0]), (self.rect.bottomleft[1]))

        for sprite in group.sprites():
            if sprite.rect.collidepoint(test_point):
                return False

        return True

    # Returns true if a ledge is on right of walker
    def ledge_right(self, group):
        # Just below and left of enemy.
        test_point = ((self.rect.bottomright[0]), (self.rect.bottomright[1]))

        for sprite in group.sprites():
            if sprite.rect.collidepoint(test_point):
                return False

        return True
            
            
