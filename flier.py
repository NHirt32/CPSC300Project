import pygame
import enemy #Inherits functionality from enemy

class Flier(enemy.Enemy):

    def __init__(self, pos):
        enemy.Enemy.__init__(self, [["assets/birds.png"]], pos)

    def update(self, group):
        if (self.edge_detect(group) == False): # If the enemy is not colliding with a solid
            self.move_x(self.move_int, group)
        else: # If the enemy is colliding with a solid
            self.move_int *= -1 # Turn around
            self.move_x(self.move_int, group) # Move slightly to avoid being stuck on the wall