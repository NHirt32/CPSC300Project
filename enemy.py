import pygame
import entity #Inherits functionality from entity

class Enemy(entity.Entity):

    def __init__(self,enemyPic , pos): # Constructor for generic enemy, jumping/gravity not currently defined
        entity.Entity.__init__(self, [[enemyPic]], pos)
        self.speed = 7
        self.boing = 0  # Also known as upward momentum.
        self.dive = 0  # downward momentum
        self.right_momentum = 0
        self.left_momentum = 0
        self.move_int = 1; # int used to track which direction an enemy object is moving

    def edge_detect(self,group):  # Returns true if the enemy object is about to touch a wall
        if self.touching_right(group) == True:
            return True
        elif self.touching_left(group) == True:
            return True
        else:
            return False

    def reverse_direction(self):
        self.move_int *= -1;

    def collided_with(self, group): # Prevents enemies from walking into walls?
        if pygame.sprite.spritecollideany(self, group) != None:
            return True
