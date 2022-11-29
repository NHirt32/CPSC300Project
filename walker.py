import pygame
import enemy #Inherits functionality from enemy

class Walker(enemy.Enemy):
    """The Walker class extends an enemy to give the functionality walkers should have.
    This is mostly just gravity."""
    def __init__(self, pos):
        """Constructor for a Walker.
.
        :param pos: a position as a tuple."""
        enemy.Enemy.__init__(self, [["assets/walker1_1.png", "assets/walker3_1.png", "assets/walker1_1.png",
                                     "assets/walker3_2.png"],
                                    ["assets/walker2_1.png", "assets/walker4_1.png", "assets/walker2_1.png",
                                     "assets/walker4_2.png"],
                                    ["assets/walker1_1.png", "assets/walker1_1.png"],
                                    ["assets/walker2_1.png", "assets/walker2_1.png"]
                                    ], pos)
        self.gravity = -100  # Defines max fall speed, MUST BE NEGATIVE
        self.vertical_momentum = 0
        self.ledge_offset = 0
        self.speed = 4

        # Directions
        self.WALKING_RIGHT = 0
        self.WALKING_LEFT = 1
        self.FALLING_RIGHT = 2
        self.FALLING_LEFT = 3

    def gravity_handler(self, group):
        """gravity_handler() handles gravity for the enemy.

        :param group: the group to disable collisions for."""
        # if falling
        if (not self.touching_ground(group)):
            if self.vertical_momentum <= 0:
                self.v_move_y(1, abs(self.vertical_momentum), group)
                if (self.vertical_momentum < self.gravity):
                    self.vertical_momentum += 1
                else:
                    self.vertical_momentum -= 1

    def update(self, group):
        """update() handles all movement for the enemy.

        :param group: the group to disable collisions for."""
        # Do nothing.
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
        self.update_direction(group)

    def ledge_left(self, group):
        """ledge_left() detects if a ledge is on the left of the walker.

        :param group: the group to test for collisions.
        :returns: true if a ledge is on the left of the walker."""
        # Just below and left of enemy.
        test_point = ((self.rect.bottomleft[0]), (self.rect.bottomleft[1]))

        for sprite in group.sprites():
            if sprite.rect.collidepoint(test_point):
                return False

        return True

    def ledge_right(self, group):
        """ledge_right() detects if a ledge is on the right of the walker.

        :param group: the group to test for collisions.
        :returns: true if a ledge is on the right of the walker."""
        # Just below and left of enemy.
        test_point = ((self.rect.bottomright[0]), (self.rect.bottomright[1]))

        for sprite in group.sprites():
            if sprite.rect.collidepoint(test_point):
                return False

        return True

    def update_direction(self, group):
        """update_direction() updates the next direction of the walker based on its touching status, its move int,
         and its fields.

         :param group: the group to test for touching."""
        if self.touching_ground(group):
            if self.move_int == 1:
                self.next_direction = self.WALKING_RIGHT
            else:
                self.next_direction = self.WALKING_LEFT
        else:
            if self.move_int == 1:
                self.next_direction = self.FALLING_RIGHT
            else:
                self.next_direction = self.FALLING_LEFT

