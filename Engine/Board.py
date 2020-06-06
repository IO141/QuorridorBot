import Engine.Coordinate as Coord
import Engine.Tile as Tile
from Engine.PlayerMove import PlayerMove

"""
Board class
Used to keep track of the game state
"""


class Board:

    def __init__(self, dim): # dim must be even number >= 10
        self.dimensions = dim
        self._homes = self._compute_player_homes()
        self._goals = self._compute_player_goals()
        self.__init_board()

    def __eq__(self, other):
        if isinstance(other, Board):
            return self.dimensions == other.dimensions \
                   and self.homes == other.homes \
                   and self.players == other.players \
                   and self.board == other.board
        return False

    def __init_board(self):
        self._board = []
        for i in range(0, self.dimensions):
            board_lst = []
            for j in range(0, self.dimensions):
                tile = self.__init_tile(Tile.Tile(Coord.Coordinate(i, j), [None, None, None, None]))
                board_lst.append(tile)
            self._board.append(board_lst)

        self._players = [None, None, None, None]
        self.__init_players()

    def __init_tile(self, tile):
        row = tile.coordinate.row
        column = tile.coordinate.column

        if row - 1 >= 0:
            Tile.Tile.add_neighbor(tile, Tile.NORTH, Coord.Coordinate(row - 1, column))
        if row + 1 < self._dimensions:
            Tile.Tile.add_neighbor(tile, Tile.SOUTH, Coord.Coordinate(row + 1, column))
        if column - 1 >= 0:
            Tile.Tile.add_neighbor(tile, Tile.EAST, Coord.Coordinate(row, column - 1))
        if column + 1 < self._dimensions:
            Tile.Tile.add_neighbor(tile, Tile.WEST, Coord.Coordinate(row, column + 1))

        return tile

    def __init_players(self):
        for index, coord in enumerate(self._homes):
            self.tile_at_coord(coord.row, coord.column).occupant = index
            self.update_player_coordinates(index, coord)

    def _compute_player_homes(self):
        return [
            Coord.Coordinate(0, self.dimensions // 2),                      # P1 top
            Coord.Coordinate(self.dimensions - 1, self.dimensions // 2),    # P2 bottom
            Coord.Coordinate(self.dimensions // 2, 0),                      # P3 left
            Coord.Coordinate(self.dimensions // 2, self.dimensions - 1)     # P4 right
        ]

    # TODO test
    def _compute_player_goals(self):
        goal0 = [Coord.Coordinate(self.homes[0].row, row_col) for row_col in range(0, self.dimensions)]
        goal1 = [Coord.Coordinate(self.homes[1].row, row_col) for row_col in range(0, self.dimensions)]
        goal2 = [Coord.Coordinate(row_col, self.homes[2].column) for row_col in range(0, self.dimensions)]
        goal3 = [Coord.Coordinate(row_col, self.homes[3].column) for row_col in range(0, self.dimensions)]

        return [goal0, goal1, goal2, goal3]

    def _compute_static_valid_wall(self, is_horizontal, coord_start):
        if is_horizontal and (
                coord_start.row <= 0
                or coord_start.row >= self.dimensions - 1
                or coord_start.column < 0
                or coord_start.column >= self.dimensions - 2
        ):
            return False
        elif not is_horizontal and (
                coord_start.row < 0
                or coord_start.row >= self.dimensions - 2
                or coord_start.column <= 0
                or coord_start.column >= self.dimensions - 1
        ):
            return False
        return True

    def _compute_dynamic_valid_wall(self, is_horizontal, coord_start):
        if is_horizontal and (
            # bottom
            self.board[coord_start.row][coord_start.column].neighbors[Tile.NORTH] is None
            or self.board[coord_start.row][coord_start.column + 1].neighbors[Tile.NORTH] is None
        ):
            return False
        elif not is_horizontal and (
            # right
            self.board[coord_start.row][coord_start.column].neighbors[Tile.EAST] is None
            or self.board[coord_start.row + 1][coord_start.column].neighbors[Tile.EAST] is None
        ):
            return False
        return True

    @property
    def board(self):
        return self._board

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, dim):
        if not hasattr(self, '_dimension'):
            dim += 1 if dim % 2 != 0 else 0
            dim = 10 if dim < 10 else dim
            self._dimensions = dim

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, pid_coord):
        try:
            pid, coordinate = pid_coord
        except ValueError:
            raise ValueError("Pass an iterable with two items.")
        else:
            self._players[pid] = coordinate

    @property
    def homes(self):
        return self._homes

    @homes.setter
    def homes(self, lst):
        if not hasattr(self, '_homes') and isinstance(lst, list):
            self._homes = lst

    @property
    def goals(self):
        return self._goals

    def tile_at_coord(self, row, column):
        return self._board[row][column]

    def update_player_coordinates(self, pid, coordinate):
        self.players = pid, coordinate

    def compute_all_valid_horizontal_walls(self):
        valid_walls = []
        for i in range(0, self.dimensions):
            for j in range(0, self.dimensions):
                coord = Coord.Coordinate(i, j)

                if self._compute_static_valid_wall(True, coord) and self._compute_dynamic_valid_wall(True, coord):
                    valid_walls.append(coord)

        return valid_walls

    def compute_all_valid_vertical_walls(self):
        valid_walls = []
        for i in range(0, self.dimensions):
            for j in range(0, self.dimensions):
                coord = Coord.Coordinate(i, j)

                if self._compute_static_valid_wall(False, coord) and self._compute_dynamic_valid_wall(False, coord):
                    valid_walls.append(coord)

        return valid_walls

    def place_wall(self, is_horizontal, coord_start):
        if not self._compute_static_valid_wall(is_horizontal, coord_start):
            raise ValueError("Wall placed out of bounds.")
        elif not self._compute_dynamic_valid_wall(is_horizontal, coord_start):
            raise ValueError("Wall placed on another wall.")
        else:
            if is_horizontal and coord_start.column != self.dimensions - 1:
                top1 = self.board[coord_start.row - 1][coord_start.column]
                bottom1 = self.board[coord_start.row][coord_start.column]
                Tile.Tile.remove_neighbor(top1, Tile.SOUTH)
                Tile.Tile.remove_neighbor(bottom1, Tile.NORTH)

                top2 = self.board[coord_start.row - 1][coord_start.column + 1]
                bottom2 = self.board[coord_start.row][coord_start.column + 1]
                Tile.Tile.remove_neighbor(top2, Tile.SOUTH)
                Tile.Tile.remove_neighbor(bottom2, Tile.NORTH)
            else:
                left1 = self.board[coord_start.row][coord_start.column - 1]
                right1 = self.board[coord_start.row][coord_start.column]
                Tile.Tile.remove_neighbor(left1, Tile.WEST)
                Tile.Tile.remove_neighbor(right1, Tile.EAST)

                left2 = self.board[coord_start.row + 1][coord_start.column - 1]
                right2 = self.board[coord_start.row + 1][coord_start.column]
                Tile.Tile.remove_neighbor(left2, Tile.WEST)
                Tile.Tile.remove_neighbor(right2, Tile.EAST)

    def undo_wall(self, is_horizontal, coord_start):
        if not self._compute_static_valid_wall(is_horizontal, coord_start):
            raise ValueError("No wall to undo out of bounds.")
        else:
            if is_horizontal:
                top1 = self.board[coord_start.row - 1][coord_start.column]
                bottom1 = self.board[coord_start.row][coord_start.column]
                Tile.Tile.add_neighbor(top1, Tile.SOUTH, bottom1.coordinate)
                Tile.Tile.add_neighbor(bottom1, Tile.NORTH, top1.coordinate)

                top2 = self.board[coord_start.row - 1][coord_start.column + 1]
                bottom2 = self.board[coord_start.row][coord_start.column + 1]
                Tile.Tile.add_neighbor(top2, Tile.SOUTH, bottom2.coordinate)
                Tile.Tile.add_neighbor(bottom2, Tile.NORTH, top2.coordinate)
            else:
                left1 = self.board[coord_start.row][coord_start.column - 1]
                right1 = self.board[coord_start.row][coord_start.column]
                Tile.Tile.add_neighbor(left1, Tile.WEST, right1.coordinate)
                Tile.Tile.add_neighbor(right1, Tile.EAST, left1.coordinate)

                left2 = self.board[coord_start.row + 1][coord_start.column - 1]
                right2 = self.board[coord_start.row + 1][coord_start.column]
                Tile.Tile.add_neighbor(left2, Tile.WEST, right2.coordinate)
                Tile.Tile.add_neighbor(right2, Tile.EAST, left2.coordinate)
