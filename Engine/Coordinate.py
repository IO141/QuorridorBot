
"""
Coordinate class
Will be used to easily reference coordinates on the board
"""


class Coordinate:

    def __init__(self, x=None, y=None, coordinate=None):
        if coordinate is not None:
            self._x = coordinate.row
            self._y = coordinate.column
        elif x is not None and y is not None:
            self._x = x
            self._y = y
        else:
            self._x = -1
            self._y = -1

    def __str__(self):
        return f'({self._x}, {self._y})'

    def __eq__(self, other):
        if isinstance(other, Coordinate):
            return self._x == other.row and self._y == other.column
        return False

    def __hash__(self):
        return hash(repr(self))

    @property
    def row(self):
        return self._x

    @property
    def column(self):
        return self._y

    @staticmethod
    def is_horizontal(coord1, coord2):
        return coord1.row == coord2.row
