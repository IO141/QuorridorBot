from Engine.Coordinate import Coordinate

"""
Player class
Handles player interactions with the game
"""


class Player:

    def __init__(self, pid, walls, homes, goals):
        if pid <= 0:
            raise ValueError("Invalid player id, cannot be <= 0.")
        if pid > len(homes) or pid > len(goals):
            raise ValueError("Invalid player id, cannot be > len of homes/goals.")

        self._my_id = pid
        self._walls_left = walls
        self._location = homes[self._my_id - 1]
        self._goal = goals[self._my_id - 1]

        id_tup = self._compute_ids()
        self._enemy_id = id_tup[0]
        self._other_ids = [id_tup[1], id_tup[2]] if len(homes) > 2 else []

    def __str__(self):
        return f'Player {self._my_id} has {self._walls_left} walls left'

    def _compute_ids(self):
        if self._my_id == 1:
            return 2, 3, 4
        elif self._my_id == 2:
            return 1, 3, 4
        elif self._my_id == 3:
            return 4, 1, 2
        elif self._my_id == 4:
            return 3, 1, 2

    @property
    def pid(self):
        return self._my_id

    @property
    def enemy_id(self):
        return self._enemy_id

    @property
    def other_ids(self):
        return self._other_ids

    @property
    def walls(self):
        return self._walls_left

    @walls.setter
    def walls(self, remove):
        if remove:
            self._walls_left -= 1
        else:
            self._walls_left += 1

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, new_coordinate):
        self._location = new_coordinate

    @property
    def goal(self):
        return self._goal

