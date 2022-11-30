import entity #Inherits functionality from entity

class Enemy(entity.Entity):
    """The Enemy class extends an entity to give the functionality enemies should have,
    like edge detection and whether the enemy died."""

    def __init__(self, enemyPic , pos):
        """Constructor for an Enemy.

        :param enemyPic: a list of lists of strings that are filepaths to images.
        :param pos: a position as a tuple."""
        entity.Entity.__init__(self, enemyPic, pos)
        self.speed = 7
        self.move_int = -1 # int used to track which direction an enemy object is moving

    def edge_detect(self, group):
        """edge_detect() returns whether the enemy object is touching left or right a sprite in a group.

        :param group: the passed group to test for collisions.
        :returns: true if touching wall."""
        if self.touching_right(group) == True:
            return True
        elif self.touching_left(group) == True:
            return True
        else:
            return False

    def reverse_direction(self):
        """reverse_direction() changes the movement direction of an enemy."""
        self.move_int *= -1

    def died(self, group):
        """died() returns whether the enemy is touching above a sprite in a group.

        :param group: the passed group to test collisions for.
        :returns: true if enemy is touching above a sprite in a group."""
        if self.touching_roof(group):
            # If the top of enemy collided with player
            return True
        else:
            return False