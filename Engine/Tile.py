"""
Tile class
Used to define unique locations on a game board
"""

NORTH = 0
SOUTH = 2
WEST = 1
EAST = 3


class Tile:

    def __init__(self, coordinate, neighbors):
        self._coordinate = coordinate
        self._neighbors = neighbors
        self._occupantID = -1

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.coordinate == other.coordinate \
                   and self.neighbors == other.neighbors \
                   and self.occupant == other.occupant
        return False

    @property
    def neighbors(self):
        """
        Neighbors are Coordinate locations adjacent to this Tile in a list.
        0 – North ( above )
        1 – West  ( right )
        2 – South ( below )
        3 – East  ( left  )
        :return: Current neighbors of this Tile as a list
        """
        return self._neighbors

    @neighbors.setter
    def neighbors(self, dir_coord):
        """
        Add/Remove a neighbor.
        :param dir_coord: The direction to add/remove, the coord to add
        """
        try:
            direction, coordinate = dir_coord
        except ValueError:
            raise ValueError("Pass an iterable with two items.")
        else:
            if self._neighbors[direction] is None:
                self._neighbors[direction] = coordinate
            else:
                self._neighbors[direction] = None

    @property
    def occupant(self):
        """
        This shows the ID of the Player on this Tile or -1 if none is present.
        :return: The ID of the Tile's occupant
        """
        return self._occupantID

    @occupant.setter
    def occupant(self, oid):
        self._occupantID = oid

    @property
    def coordinate(self):
        return self._coordinate

    @staticmethod
    def end_occupancy(tile):
        tile.occupant = -1

    @staticmethod
    def remove_neighbor(tile, direction):
        tile.neighbors = direction, None

    @staticmethod
    def add_neighbor(tile, direction, neighbor):
        tile.neighbors = direction, neighbor
