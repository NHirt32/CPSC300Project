import pygame
import enemy #Inherits functionality from enemy

class Flier(enemy.Enemy):
    """The Flier class extends an enemy to give the functionality fliers should have.
    This is mostly to not apply gravity to them."""
    def __init__(self, pos):
        """Constructor for a Flier.
.
        :param pos: a position as a tuple."""
        enemy.Enemy.__init__(self,
                 [["assets/ghost1_1.png", "assets/ghost1_2.png", "assets/ghost1_3.png", "assets/ghost1_4.png",
                    "assets/ghost1_5.png", "assets/ghost1_6.png", "assets/ghost1_7.png", "assets/ghost1_6.png",
                    "assets/ghost1_5.png","assets/ghost1_4.png","assets/ghost1_3.png","assets/ghost1_2.png",
                    "assets/ghost1_1.png"],
                     ["assets/ghost2_1.png", "assets/ghost2_2.png", "assets/ghost2_3.png", "assets/ghost2_4.png",
                    "assets/ghost2_5.png", "assets/ghost2_6.png", "assets/ghost2_7.png", "assets/ghost2_6.png",
                    "assets/ghost2_5.png", "assets/ghost2_4.png", "assets/ghost2_3.png", "assets/ghost2_2.png",
                    "assets/ghost2_1.png", ]],
                             pos)
        self.speed = 3

        # Directions
        self.RIGHT = 0
        self.LEFT = 1

    def update(self, group):
        """update() handles all the movement and animation for the flier."""
        if (self.edge_detect(group) == False): # If the enemy is not colliding with a solid
            self.move_x(self.move_int, group)
        else: # If the enemy is colliding with a solid
            self.move_int *= -1 # Turn around
            self.move_x(self.move_int, group) # Move slightly to avoid being stuck on the wall

        self.update_direction()

    def update_direction(self):
        """update_direction() handles determining the fliers next animation."""
        if self.move_int == 1:
            self.next_direction = self.RIGHT
        else:
            self.next_direction = self.LEFT
