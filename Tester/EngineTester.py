import unittest
import copy
import Engine.Tile as Ti
from Engine.Coordinate import Coordinate
from Engine.Tile import Tile
from Engine.Board import Board
from Engine.Player import Player
from Engine.PlayerMove import PlayerMove
from AI.Moves import Moves


class CoordinateTestCase(unittest.TestCase):
    """Tests for 'Coordinate.py.'"""

    def test_is_xy_correct_input1(self):
        coord = Coordinate(1, 2)
        self.assertEqual(1, coord.row)
        self.assertEqual(2, coord.column)

    def test_is_xy_correct_input2(self):
        coord1 = Coordinate(1, 2)
        coord2 = Coordinate(coordinate=coord1)
        self.assertTrue(coord1 == coord2)

    def test_is_xy_correct_input3(self):
        coord1 = Coordinate()
        self.assertEqual(-1, coord1.row)
        self.assertEqual(-1, coord1.column)

    def test_is_str_correct(self):
        coord = Coordinate(1, 2)
        msg = '(1, 2)'
        self.assertEqual(str(coord), msg)

    def test_is_horizontal_correct(self):
        coord1 = Coordinate(1, 2)
        coordh = Coordinate(1, 4)
        coordv = Coordinate(3, 2)
        self.assertTrue(Coordinate.is_horizontal(coord1, coordh))
        self.assertFalse(Coordinate.is_horizontal(coord1, coordv))


class TileTestCase(unittest.TestCase):
    """Tests for 'Tile.py'."""

    def test_sanity_confirm_tile_directions_are_different(self):
        self.assertTrue(Ti.NORTH != Ti.SOUTH)
        self.assertTrue(Ti.NORTH != Ti.EAST)
        self.assertTrue(Ti.NORTH != Ti.WEST)

        self.assertTrue(Ti.SOUTH != Ti.NORTH)
        self.assertTrue(Ti.SOUTH != Ti.EAST)
        self.assertTrue(Ti.SOUTH != Ti.WEST)

        self.assertTrue(Ti.EAST != Ti.NORTH)
        self.assertTrue(Ti.EAST != Ti.SOUTH)
        self.assertTrue(Ti.EAST != Ti.WEST)

        self.assertTrue(Ti.WEST != Ti.NORTH)
        self.assertTrue(Ti.WEST != Ti.SOUTH)
        self.assertTrue(Ti.WEST != Ti.EAST)

    def test_is_eq_correct(self):
        neighbors1 = [Coordinate(1, 2), None, None, None]
        tile1 = Tile(coordinate=Coordinate(1, 2))
        tile2 = Tile(coordinate=Coordinate(1, 2))
        tile3 = Tile(coordinate=Coordinate(1, 3))
        tile4 = Tile(coordinate=Coordinate(1, 2), neighbors=neighbors1)
        self.assertTrue(tile1 == tile2)
        self.assertFalse(tile1 == tile3)
        self.assertFalse(tile3 == tile4)

    def test_is_coordinate_correct(self):
        coord = Coordinate(1, 2)
        tile1 = Tile(coordinate=coord)
        self.assertTrue(tile1.coordinate == coord)

    def test_is_neighbors_correct_input1(self):
        coord = Coordinate(1, 2)
        neighbors = [None, None, None, None]
        tile1 = Tile(coordinate=coord)
        self.assertTrue(tile1.neighbors == neighbors)
        self.assertTrue(tile1.coordinate == coord)

    def test_is_neighbors_correct_input2(self):
        coord = Coordinate(1, 2)
        neighbors2 = [coord, None, None, None]
        tile1 = Tile(coordinate=coord)
        tile2 = Tile(coordinate=coord, neighbors=neighbors2)
        self.assertTrue(tile2.neighbors[0] == tile1.coordinate)

    def test_is_occupant_correct(self):
        coord = Coordinate(1, 2)
        tile1 = Tile(coordinate=coord)
        self.assertTrue(tile1.occupant == -1)

    def test_is_end_occupancy_correct(self):
        coord = Coordinate(1, 2)
        tile1 = Tile(coordinate=coord)
        tile1.occupant = 1
        Tile.end_occupancy(tile1)
        self.assertTrue(tile1.occupant == -1)

    @staticmethod
    def test_is_remove_neighbors_correct():
        coord = Coordinate(1, 2)
        neighbors1 = [coord, None, None, None]
        tile1 = Tile(coordinate=coord, neighbors=neighbors1)
        Tile.remove_neighbor(tile1, 0)


class BoardTestCase(unittest.TestCase):
    """Tests for 'Board.py'."""

    std_dim = 10

    def test_sanity_is_board_tile_obj_identical(self):
        board = Board(10)
        tile = board.tile_at_coord(1, 2)
        self.assertEqual(tile, board.board[1][2])
        tile.occupant = 1
        self.assertEqual(tile, board.board[1][2])
        self.assertTrue(tile.occupant == board.board[1][2].occupant)

    def test_board_equality(self):
        board1 = Board(10)
        board2 = Board(10)

        self.assertTrue(board1 == board2)

        board2._dimensions = 3
        self.assertFalse(board1 == board2)
        board2._dimensions = board1._dimensions
        self.assertTrue(board1 == board2)

        board2._homes[0] = None
        self.assertFalse(board1 == board2)
        board2._homes[0] = board1._homes[0]
        self.assertTrue(board1 == board2)

        board2._players[0] = None
        self.assertFalse(board1 == board2)
        board2._players[0] = board1._players[0]
        self.assertTrue(board1 == board2)

        board2.place_wall(True, Coordinate(5, 5))
        self.assertFalse(board1 == board2)
        board2.undo_wall(True, Coordinate(5, 5))
        self.assertTrue(board1 == board2)

    def test_is_dim_correct(self):
        # dim should correct to 10
        dim = 9
        board = Board(dim)
        self.assertFalse(board.dimensions == dim)
        self.assertTrue(board.dimensions == 10)

        # dim should correct to 10
        dim = 5
        board = Board(dim)
        self.assertFalse(board.dimensions == dim)
        self.assertTrue(board.dimensions == 10)

        # dim should correct to 12
        dim = 11
        board = Board(dim)
        self.assertFalse(board.dimensions == dim)
        self.assertTrue(board.dimensions == 12)

        # dim should stay at 14
        dim = 14
        board = Board(dim)
        self.assertTrue(board.dimensions == dim)

    def test_is_homes_correct(self):
        board = Board(BoardTestCase.std_dim)
        homes = board._compute_player_homes()
        check = [
            Coordinate(0, BoardTestCase.std_dim // 2),
            Coordinate(BoardTestCase.std_dim - 1, BoardTestCase.std_dim // 2),
            Coordinate(BoardTestCase.std_dim // 2, 0),
            Coordinate(BoardTestCase.std_dim // 2, BoardTestCase.std_dim - 1)
        ]
        self.assertTrue(homes == check)

    def test_is_players_home_correct(self):
        board = Board(BoardTestCase.std_dim)
        homes = [
            Coordinate(0, BoardTestCase.std_dim // 2),
            Coordinate(BoardTestCase.std_dim - 1, BoardTestCase.std_dim // 2),
            Coordinate(BoardTestCase.std_dim // 2, 0),
            Coordinate(BoardTestCase.std_dim // 2, BoardTestCase.std_dim - 1)
        ]
        self.assertTrue(homes == board.players)

    def test_is_board_tiles_init(self):
        board = Board(BoardTestCase.std_dim)
        self.assertTrue(board._dimensions == BoardTestCase.std_dim)
        self.assertTrue(sum(len(t) for t in board.board) == BoardTestCase.std_dim ** 2)
        self.assertTrue(
            all([(isinstance(t.coordinate, Coordinate) or t.coordinate is None) for t in tc] for tc in board.board))

    def test_is_tile_coord_correct(self):
        board = Board(BoardTestCase.std_dim)
        coord = Coordinate(1, 2)
        tile12 = board.tile_at_coord(1, 2)
        self.assertTrue(isinstance(tile12, Tile))
        self.assertTrue(coord.row == tile12.coordinate.row and coord.column == tile12.coordinate.column)

    def test_is_static_valid_walls_correct(self):
        board = Board(BoardTestCase.std_dim)

        # Horizontal checks
        self.assertFalse(board._compute_static_valid_wall(True, Coordinate(0, 2)))        # Bad lower row
        self.assertFalse(board._compute_static_valid_wall(True, Coordinate(2, -1)))       # Bad lower column
        self.assertFalse(
            board._compute_static_valid_wall(True, Coordinate(BoardTestCase.std_dim - 1, 2)))  # Bad upper row
        self.assertFalse(
            board._compute_static_valid_wall(True, Coordinate(2, BoardTestCase.std_dim - 2)))  # Bad upper column

        self.assertTrue(board._compute_static_valid_wall(True, Coordinate(1, 2)))         # Good lower row
        self.assertTrue(board._compute_static_valid_wall(True, Coordinate(2, 0)))         # Good lower column
        self.assertTrue(
            board._compute_static_valid_wall(True, Coordinate(BoardTestCase.std_dim - 2, 2)))   # Good upper row
        self.assertTrue(
            board._compute_static_valid_wall(True, Coordinate(2, BoardTestCase.std_dim - 3)))   # Good upper column

        # Vertical checks
        self.assertFalse(board._compute_static_valid_wall(False, Coordinate(-1, 1)))       # Bad lower row
        self.assertFalse(board._compute_static_valid_wall(False, Coordinate(1, 0)))        # Bad lower column
        self.assertFalse(
            board._compute_static_valid_wall(False, Coordinate(BoardTestCase.std_dim - 2, 3)))  # Bad upper row
        self.assertFalse(
            board._compute_static_valid_wall(False, Coordinate(3, BoardTestCase.std_dim - 1)))  # Bad upper column

        self.assertTrue(board._compute_static_valid_wall(False, Coordinate(0, 1)))         # Good lower row
        self.assertTrue(board._compute_static_valid_wall(False, Coordinate(1, 1)))         # Good lower column
        self.assertTrue(
            board._compute_static_valid_wall(False, Coordinate(BoardTestCase.std_dim - 3, 3)))   # Good upper row
        self.assertTrue(
            board._compute_static_valid_wall(False, Coordinate(3, BoardTestCase.std_dim - 2)))   # Good upper column

    def test_is_dynamic_valid_walls_correct(self):
        board = Board(BoardTestCase.std_dim)

        self.assertTrue(board._compute_dynamic_valid_wall(True, Coordinate(2, 2)))
        self.assertTrue(board._compute_dynamic_valid_wall(False, Coordinate(5, 5)))

        board.place_wall(True, Coordinate(2, 2))
        self.assertFalse(board._compute_dynamic_valid_wall(True, Coordinate(2, 2)))
        self.assertFalse(board._compute_dynamic_valid_wall(True, Coordinate(2, 3)))
        self.assertFalse(board._compute_dynamic_valid_wall(True, Coordinate(2, 1)))
        self.assertTrue(board._compute_dynamic_valid_wall(True, Coordinate(2, 0)))
        self.assertTrue(board._compute_dynamic_valid_wall(True, Coordinate(2, 4)))

        board.place_wall(False, Coordinate(5, 5))
        self.assertFalse(board._compute_dynamic_valid_wall(False, Coordinate(5, 5)))
        self.assertFalse(board._compute_dynamic_valid_wall(False, Coordinate(6, 5)))
        self.assertFalse(board._compute_dynamic_valid_wall(False, Coordinate(4, 5)))
        self.assertTrue(board._compute_dynamic_valid_wall(False, Coordinate(3, 5)))
        self.assertTrue(board._compute_dynamic_valid_wall(False, Coordinate(7, 5)))

    def test_is_horizontal_wall_place_correct(self):
        board = Board(BoardTestCase.std_dim)
        self.assertRaises(ValueError, board.place_wall, True, Coordinate(0, 2))  # Bad coord except check

        for i in range(board.dimensions):
            for j in range(board.dimensions):
                coord = Coordinate(i, j)

                if not board._compute_static_valid_wall(True, coord):
                    continue

                self.assertTrue(board._compute_dynamic_valid_wall(True, coord))

                top1 = board.board[coord.row - 1][coord.column]
                top2 = board.board[coord.row - 1][coord.column + 1]
                bottom1 = board.board[coord.row][coord.column]
                bottom2 = board.board[coord.row][coord.column + 1]

                neighbors_top1 = copy.deepcopy(top1.neighbors)
                neighbors_top2 = copy.deepcopy(top2.neighbors)
                neighbors_bottom1 = copy.deepcopy(bottom1.neighbors)
                neighbors_bottom2 = copy.deepcopy(bottom2.neighbors)

                board.place_wall(True, coord)

                self.assertTrue(top1.neighbors[Ti.SOUTH] is None)
                self.assertTrue(top1.neighbors[Ti.NORTH] == neighbors_top1[Ti.NORTH])
                self.assertTrue(top1.neighbors[Ti.EAST] == neighbors_top1[Ti.EAST])
                self.assertTrue(top1.neighbors[Ti.WEST] == neighbors_top1[Ti.WEST])

                self.assertTrue(top2.neighbors[Ti.SOUTH] is None)
                self.assertTrue(top2.neighbors[Ti.NORTH] == neighbors_top2[Ti.NORTH])
                self.assertTrue(top2.neighbors[Ti.EAST] == neighbors_top2[Ti.EAST])
                self.assertTrue(top2.neighbors[Ti.WEST] == neighbors_top2[Ti.WEST])

                self.assertTrue(bottom1.neighbors[Ti.NORTH] is None)
                self.assertTrue(bottom1.neighbors[Ti.SOUTH] == neighbors_bottom1[Ti.SOUTH])
                self.assertTrue(bottom1.neighbors[Ti.EAST] == neighbors_bottom1[Ti.EAST])
                self.assertTrue(bottom1.neighbors[Ti.WEST] == neighbors_bottom1[Ti.WEST])

                self.assertTrue(bottom2.neighbors[Ti.NORTH] is None)
                self.assertTrue(bottom2.neighbors[Ti.SOUTH] == neighbors_bottom2[Ti.SOUTH])
                self.assertTrue(bottom2.neighbors[Ti.EAST] == neighbors_bottom2[Ti.EAST])
                self.assertTrue(bottom2.neighbors[Ti.WEST] == neighbors_bottom2[Ti.WEST])

                board.undo_wall(True, coord)

    def test_is_horizontal_wall_undo_correct(self):
        board = Board(BoardTestCase.std_dim)
        self.assertRaises(ValueError, board.place_wall, True, Coordinate(0, 2))  # Bad coord except check

        for i in range(board.dimensions):
            for j in range(board.dimensions):
                coord = Coordinate(i, j)

                if not board._compute_static_valid_wall(True, coord):
                    continue

                top1 = board.board[coord.row - 1][coord.column]
                top2 = board.board[coord.row - 1][coord.column + 1]
                bottom1 = board.board[coord.row][coord.column]
                bottom2 = board.board[coord.row][coord.column + 1]

                neighbors_top1 = copy.deepcopy(top1.neighbors)
                neighbors_top2 = copy.deepcopy(top2.neighbors)
                neighbors_bottom1 = copy.deepcopy(bottom1.neighbors)
                neighbors_bottom2 = copy.deepcopy(bottom2.neighbors)

                board.place_wall(True, coord)

                self.assertTrue(top1.neighbors[Ti.SOUTH] is None)
                self.assertTrue(top1.neighbors[Ti.NORTH] == neighbors_top1[Ti.NORTH])
                self.assertTrue(top1.neighbors[Ti.EAST] == neighbors_top1[Ti.EAST])
                self.assertTrue(top1.neighbors[Ti.WEST] == neighbors_top1[Ti.WEST])

                self.assertTrue(top2.neighbors[Ti.SOUTH] is None)
                self.assertTrue(top2.neighbors[Ti.NORTH] == neighbors_top2[Ti.NORTH])
                self.assertTrue(top2.neighbors[Ti.EAST] == neighbors_top2[Ti.EAST])
                self.assertTrue(top2.neighbors[Ti.WEST] == neighbors_top2[Ti.WEST])

                self.assertTrue(bottom1.neighbors[Ti.NORTH] is None)
                self.assertTrue(bottom1.neighbors[Ti.SOUTH] == neighbors_bottom1[Ti.SOUTH])
                self.assertTrue(bottom1.neighbors[Ti.EAST] == neighbors_bottom1[Ti.EAST])
                self.assertTrue(bottom1.neighbors[Ti.WEST] == neighbors_bottom1[Ti.WEST])

                self.assertTrue(bottom2.neighbors[Ti.NORTH] is None)
                self.assertTrue(bottom2.neighbors[Ti.SOUTH] == neighbors_bottom2[Ti.SOUTH])
                self.assertTrue(bottom2.neighbors[Ti.EAST] == neighbors_bottom2[Ti.EAST])
                self.assertTrue(bottom2.neighbors[Ti.WEST] == neighbors_bottom2[Ti.WEST])

                board.undo_wall(True, coord)

                self.assertTrue(top1.neighbors[Ti.SOUTH] == neighbors_top1[Ti.SOUTH])
                self.assertTrue(top2.neighbors[Ti.SOUTH] == neighbors_top2[Ti.SOUTH])
                self.assertTrue(bottom1.neighbors[Ti.NORTH] == neighbors_bottom1[Ti.NORTH])
                self.assertTrue(bottom2.neighbors[Ti.NORTH] == neighbors_bottom2[Ti.NORTH])

    def test_is_vertical_wall_place_correct(self):
        board = Board(BoardTestCase.std_dim)
        self.assertRaises(ValueError, board.place_wall, False, Coordinate(1, 0))  # Bad coord except check

        for i in range(board.dimensions):
            for j in range(board.dimensions):
                coord = Coordinate(i, j)

                if not board._compute_static_valid_wall(False, coord):
                    continue

                self.assertTrue(board._compute_dynamic_valid_wall(False, coord))

                left1 = board.board[coord.row][coord.column - 1]
                left2 = board.board[coord.row + 1][coord.column - 1]
                right1 = board.board[coord.row][coord.column]
                right2 = board.board[coord.row + 1][coord.column]

                neighbors_left1 = copy.deepcopy(left1.neighbors)
                neighbors_left2 = copy.deepcopy(left2.neighbors)
                neighbors_right1 = copy.deepcopy(right1.neighbors)
                neighbors_right2 = copy.deepcopy(right2.neighbors)

                board.place_wall(False, coord)

                self.assertTrue(left1.neighbors[Ti.WEST] is None)
                self.assertTrue(left1.neighbors[Ti.EAST] == neighbors_left1[Ti.EAST])
                self.assertTrue(left1.neighbors[Ti.NORTH] == neighbors_left1[Ti.NORTH])
                self.assertTrue(left1.neighbors[Ti.SOUTH] == neighbors_left1[Ti.SOUTH])

                self.assertTrue(left2.neighbors[Ti.WEST] is None)
                self.assertTrue(left2.neighbors[Ti.EAST] == neighbors_left2[Ti.EAST])
                self.assertTrue(left2.neighbors[Ti.NORTH] == neighbors_left2[Ti.NORTH])
                self.assertTrue(left2.neighbors[Ti.SOUTH] == neighbors_left2[Ti.SOUTH])

                self.assertTrue(right1.neighbors[Ti.EAST] is None)
                self.assertTrue(right1.neighbors[Ti.WEST] == neighbors_right1[Ti.WEST])
                self.assertTrue(right1.neighbors[Ti.NORTH] == neighbors_right1[Ti.NORTH])
                self.assertTrue(right1.neighbors[Ti.SOUTH] == neighbors_right1[Ti.SOUTH])

                self.assertTrue(right2.neighbors[Ti.EAST] is None)
                self.assertTrue(right2.neighbors[Ti.WEST] == neighbors_right2[Ti.WEST])
                self.assertTrue(right2.neighbors[Ti.NORTH] == neighbors_right2[Ti.NORTH])
                self.assertTrue(right2.neighbors[Ti.SOUTH] == neighbors_right2[Ti.SOUTH])

                board.undo_wall(False, coord)

    def test_is_vertical_wall_undo_correct(self):
        board = Board(BoardTestCase.std_dim)
        self.assertRaises(ValueError, board.place_wall, False, Coordinate(1, 0))  # Bad coord except check

        for i in range(board.dimensions):
            for j in range(board.dimensions):
                coord = Coordinate(i, j)

                if not board._compute_static_valid_wall(False, coord):
                    continue

                left1 = board.board[coord.row][coord.column - 1]
                left2 = board.board[coord.row + 1][coord.column - 1]
                right1 = board.board[coord.row][coord.column]
                right2 = board.board[coord.row + 1][coord.column]

                neighbors_left1 = copy.deepcopy(left1.neighbors)
                neighbors_left2 = copy.deepcopy(left2.neighbors)
                neighbors_right1 = copy.deepcopy(right1.neighbors)
                neighbors_right2 = copy.deepcopy(right2.neighbors)

                board.place_wall(False, coord)
                board.undo_wall(False, coord)

                self.assertTrue(left1.neighbors[Ti.WEST] == neighbors_left1[Ti.WEST])
                self.assertTrue(left2.neighbors[Ti.WEST] == neighbors_left2[Ti.WEST])
                self.assertTrue(right1.neighbors[Ti.EAST] == neighbors_right1[Ti.EAST])
                self.assertTrue(right2.neighbors[Ti.EAST] == neighbors_right2[Ti.EAST])


class PlayerTestCase(unittest.TestCase):
    """Tests for 'Player.py'."""

    def test_is_pid_flag_working(self):
        # Test pid too low
        self.assertRaises(ValueError, Player, 0, 10, [None, None], [None, None])
        self.assertRaises(ValueError, Player, -1, 10, [None, None], [None, None])
        # Test pid too high
        self.assertRaises(ValueError, Player, 3, 10, [None, None], [None, None])
        self.assertRaises(ValueError, Player, 5, 10, [None, None, None, None], [None, None, None, None])

        try:
            Player(1, 10, [None, None], [None, None])
            Player(3, 10, [None, None, None, None], [None, None, None, None])
        except ValueError:
            self.fail("Player() raised ValueError unexpectedly.")

    def test_are_ids_correct(self):
        player1 = Player(1, 10, [None, None], [None, None])

        self.assertTrue(player1.enemy_id == 2)
        self.assertTrue(player1.other_ids == [])

        player1 = Player(1, 10, [None, None, None, None], [None, None, None, None])
        self.assertTrue(player1.enemy_id == 2)
        self.assertTrue(player1.other_ids == [3, 4])

        player2 = Player(2, 10, [None, None, None, None], [None, None, None, None])
        self.assertTrue(player2.enemy_id == 1)
        self.assertTrue(player2.other_ids == [3, 4])

        player3 = Player(3, 10, [None, None, None, None], [None, None, None, None])
        self.assertTrue(player3.enemy_id == 4)
        self.assertTrue(player3.other_ids == [1, 2])

        player4 = Player(4, 10, [None, None, None, None], [None, None, None, None])
        self.assertTrue(player4.enemy_id == 3)
        self.assertTrue(player4.other_ids == [1, 2])

    def test_is_init_params_correct(self):
        player1 = Player(1, 10, [Coordinate(0, 5), Coordinate(9, 5)], [Coordinate(9, 4), Coordinate(0, 4)])

        self.assertTrue(player1.pid == 1)
        self.assertTrue(player1.walls == 10)
        self.assertTrue(player1.location == Coordinate(0, 5))
        self.assertTrue(player1.goal == Coordinate(9, 4))

        player3 = Player(3, 10,
                         [Coordinate(0, 5), Coordinate(9, 5), Coordinate(5, 0), Coordinate(5, 9)],
                         [Coordinate(9, 4), Coordinate(0, 4), Coordinate(4, 9), Coordinate(4, 0)]
                         )

        self.assertTrue(player3.pid == 3)
        self.assertTrue(player3.walls == 10)
        self.assertTrue(player3.location == Coordinate(5, 0))
        self.assertTrue(player3.goal == Coordinate(4, 9))

        player4 = Player(4, 10,
                         [Coordinate(0, 5), Coordinate(9, 5), Coordinate(5, 0), Coordinate(5, 9)],
                         [Coordinate(9, 4), Coordinate(0, 4), Coordinate(4, 9), [Coordinate(4, 0), Coordinate(6, 0)]])

        self.assertTrue(player4.pid == 4)
        self.assertTrue(player4.walls == 10)
        self.assertTrue(player4.location == Coordinate(5, 9))
        self.assertTrue(player4.goal == [Coordinate(4, 0), Coordinate(6, 0)])

    def test_is_walls_update_correct(self):
        player = Player(1, 10, [None, None], [None, None])

        self.assertTrue(player.walls == 10)
        player.walls = True
        self.assertTrue(player.walls == 9)
        player.walls = False
        self.assertTrue(player.walls == 10)

    def test_is_str_correct(self):
        player = Player(1, 100, [None, None], [None, None])
        msg = 'Player 1 has 100 walls left'
        self.assertEqual(str(player), msg)


class PlayerMoveTestCase(unittest.TestCase):
    """Tests for 'PlayerMove.py'."""

    def test_is_eq_correct(self):
        # Test trivial eq
        move1 = PlayerMove(Coordinate(5, 5), 1, True)
        move2 = PlayerMove(Coordinate(5, 5), 1, True)
        self.assertTrue(move1 == move2)

        # Test walls not equal
        move3 = PlayerMove(Coordinate(5, 5), 1, False)
        move4 = PlayerMove(Coordinate(5, 5), 1)
        self.assertFalse(move1 == move3)
        self.assertFalse(move1 == move4)
        self.assertFalse(move3 == move4)

        # Test coordinates not equal
        move5 = PlayerMove(Coordinate(5, 6), 1, True)
        move6 = PlayerMove(Coordinate(6, 5), 1, True)
        move7 = PlayerMove(Coordinate(4, 4), 1, True)
        self.assertFalse(move1 == move5)
        self.assertFalse(move1 == move6)
        self.assertFalse(move1 == move7)

        # Test pid not equal
        move8 = PlayerMove(Coordinate(5, 5), 2, True)
        self.assertFalse(move1 == move8)

        # Test all not equal
        move9 = PlayerMove(Coordinate(4, 4), 2)
        self.assertFalse(move1 == move9)

    def test_pid_setter(self):
        move = PlayerMove(Coordinate(5, 5))
        self.assertTrue(move.player_id == -1)

        move.player_id = 0
        self.assertTrue(move.player_id == -1)
        move.player_id = 1
        self.assertTrue(move.player_id == 1)
        move.player_id = 4
        self.assertTrue(move.player_id == 4)
        move.player_id = 5
        self.assertTrue(move.player_id == 4)


class MovesTestCase(unittest.TestCase):
    """Tests for 'Moves.py'."""

    def test_is_compute_coordinate_diff_direction_correct(self):
        std_coord = Coordinate(5, 5)

        self.assertRaises(ValueError, Moves._compute_coordinate_diff_direction, std_coord, Coordinate(5, 7))
        self.assertRaises(ValueError, Moves._compute_coordinate_diff_direction, std_coord, Coordinate(7, 5))
        self.assertRaises(ValueError, Moves._compute_coordinate_diff_direction, Coordinate(5, 7), std_coord)
        self.assertRaises(ValueError, Moves._compute_coordinate_diff_direction, Coordinate(7, 5), std_coord)

        north = Moves._compute_coordinate_diff_direction(std_coord, Coordinate(4, 5))
        south = Moves._compute_coordinate_diff_direction(std_coord, Coordinate(6, 5))
        east = Moves._compute_coordinate_diff_direction(std_coord, Coordinate(5, 4))
        west = Moves._compute_coordinate_diff_direction(std_coord, Coordinate(5, 6))

        self.assertTrue(north == Ti.NORTH)
        self.assertTrue(south == Ti.SOUTH)
        self.assertTrue(east == Ti.EAST)
        self.assertTrue(west == Ti.WEST)


if __name__ == '__main__':
    unittest.main()
