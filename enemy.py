import pygame
import entity #Inherits functionality from entity

class Enemy(entity.Entity):

    def __init__(self, enemyPic , pos): # Constructor for generic enemy, jumping/gravity not currently defined
        entity.Entity.__init__(self, enemyPic, pos)
        self.speed = 7
        self.move_int = -1; # int used to track which direction an enemy object is moving
        self.death_h_offset = 5 # deals with hitpoints of enemies horizontally.
        self.death_v_offset = 4 # deals with hitpoints of enemies vertically.

    def edge_detect(self, group):  # Returns true if the enemy object is about to touch a wall
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

    def died(self, sprite):

        test_mid = (self.rect.midtop[0], (self.rect.midtop[1] - self.death_v_offset))
        test_right = ((self.rect.midtop[0] + self.death_h_offset), (self.rect.midtop[1] - self.death_v_offset))
        test_left = ((self.rect.midtop[0] - self.death_h_offset), (self.rect.midtop[1] - self.death_v_offset))

        if sprite.rect.collidepoint(test_mid) or sprite.rect.collidepoint(test_right) or \
                sprite.rect.collidepoint(test_left):
                 # If the top of enemy collided with player
            return True
        else:
            return False
