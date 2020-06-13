import Engine.Tile as Tile
from Engine.PlayerMove import PlayerMove
# from functools import lru_cache

"""
Moves class
Utility class to make available all legal moves to a Player.
"""


class Moves:
    """
    Wall moves can be computed statically, without a player ID.
    Piece moves require a player ID so are not computed in __init__.

    Wall moves can be passed between Moves instances near the same turn to save
    on compute time using the wall_moves parameter in __init__.
    """

    def __init__(self, board, wall_moves=None):
        self._board = board
        self.player_moves = None
        self.wall_moves = self._compute_all_wall_moves() if wall_moves is None else wall_moves

    def get_player_moves(self, pid, player_locations):
        self.player_moves = self._compute_all_piece_moves(pid, player_locations)

    # @lru_cache(maxsize=None)
    def _compute_all_piece_moves(self, pid, player_locations):
        piece_moves = []

        # Initial get tile neighbors
        player_coord = player_locations[pid - 1]
        player_tile = self._board.tile_at_coord(player_coord.row, player_coord.column)
        potential_coords = set([c for c in player_tile.neighbors if c is not None])

        # Figure out if special rules apply wrt other players
        if not potential_coords.isdisjoint(player_locations):
            for coord in potential_coords.intersection(player_locations):
                occupied_tile = self._board.tile_at_coord(coord.row, coord.column)

                try:
                    direction = self._compute_coordinate_diff_direction(player_coord, coord)
                    potential_coords.remove(coord)
                except ValueError:
                    continue

                if occupied_tile[direction] is not None:
                    potential_coords.add(occupied_tile[direction])
                else:
                    if direction % 2 == 0:
                        if occupied_tile[Tile.EAST] is not None:
                            potential_coords.add(occupied_tile[Tile.EAST])
                        elif occupied_tile[Tile.WEST] is not None:
                            potential_coords.add(occupied_tile[Tile.WEST])
                    else:
                        if occupied_tile[Tile.NORTH] is not None:
                            potential_coords.add(occupied_tile[Tile.NORTH])
                        elif occupied_tile[Tile.SOUTH] is not None:
                            potential_coords.add(occupied_tile[Tile.SOUTH])

        piece_moves.extend([PlayerMove(coord, pid) for coord in potential_coords])

        return piece_moves

    # @lru_cache(maxsize=None)
    def _compute_all_wall_moves(self):
        wall_moves = []

        horizontal_moves = self._board.compute_all_valid_horizontal_walls()
        for pid in range(0, len(self._board.goals)):
            for coord in horizontal_moves:
                self._board.place_wall(True, coord)

                if not self.path_exists(coord, self._board.goals[pid], self._board):
                    horizontal_moves.remove()

                self._board.undo_wall(True, coord)

        vertical_moves = self._board.compute_all_valid_vertical_walls()
        for pid in range(0, len(self._board.goals)):
            for coord in vertical_moves:
                self._board.place_wall(False, coord)

                if not self.path_exists(coord, self._board.goals[pid], self._board):
                    vertical_moves.remove()

                self._board.undo_wall(False, coord)

        wall_moves.extend([PlayerMove(move, -1, True) for move in horizontal_moves])
        wall_moves.extend([PlayerMove(move, -1, False) for move in vertical_moves])

        return wall_moves

    # @lru_cache(maxsize=None)
    def path_exists(self, coord_start, coord_end_lst, board):
        for coord_end in coord_end_lst:
            if len(self.bfs_search(coord_start, coord_end, board)) > 0:
                return True
        return False

    # @lru_cache(maxsize=None)
    def bfs_search(self, coord_start, coord_end, board):
        dispenser = [coord_start]

        predecessors = {coord_start: coord_start}

        while len(dispenser) > 0:
            coord_curr = dispenser.pop()
            if coord_curr.row == coord_end.row and coord_curr.column == coord_end.column:
                break
            for coord in board.tile_at_coord(coord_curr.row, coord_curr.column).neighbors:
                if coord not in predecessors.keys():
                    predecessors[coord] = coord_curr
                    dispenser.append(coord)

        return self.construct_path(predecessors, coord_start, coord_end)

    @staticmethod
    # @lru_cache(maxsize=None)
    def construct_path(predecessors, coord_start, coord_end):
        path = []

        if coord_end in predecessors.keys():
            coord_curr = coord_end
            while coord_curr.row != coord_start.row or coord_curr.column != coord_start.column:
                path.insert(0, coord_curr)
                coord_curr = predecessors.get(coord_curr)
            path.insert(0, coord_start)

        return path

    @staticmethod
    # @lru_cache(maxsize=None)
    def _compute_coordinate_diff_direction(center_coord, adjacent_coord):
        row_diff = center_coord.row - adjacent_coord.row
        column_diff = center_coord.column - adjacent_coord.column

        if row_diff < -1 or row_diff > 1 or column_diff < -1 or column_diff > 1:  # formerly row_diff + 1 > 2 or column_diff + 1 > 2
            raise ValueError("Coordinates are not adjacent.")
        elif row_diff == 0 and column_diff == 0:
            raise ValueError("Coordinates are identical.")

        if row_diff == 1:
            return Tile.NORTH
        elif row_diff == -1:
            return Tile.SOUTH
        if column_diff == 1:
            return Tile.EAST
        elif column_diff == -1:
            return Tile.WEST
