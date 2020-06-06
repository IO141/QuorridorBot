
"""
Player class
Handles player interactions with the game
"""


class PlayerMove:

    def __init__(self, coordinate, pid=-1, is_horizontal=None):
        self._player_id = pid
        self._coordinate = coordinate
        self._is_horizontal = is_horizontal

    def __eq__(self, other):
        if isinstance(other, PlayerMove):
            return self.player_id == other.player_id \
                   and self.coordinate == other.coordinate \
                   and self.is_horizontal == other.is_horizontal

    @property
    def player_id(self):
        """
        The ID of the player making this move.
        If no player is assigned, will be -1
        :return: The player's ID
        """
        return self._player_id

    @player_id.setter
    def player_id(self, pid):
        if not (pid < 1 or pid > 4):
            self._player_id = pid

    @property
    def coordinate(self):
        """
        The destination coordinate.
        :return: A coordinate
        """
        return self._coordinate

    @property
    def is_horizontal(self):
        """
        True if the move is a wall_move and the wall is horizontal
        False if the move is a wall_move and the wall is vertical
        None is the move is a piece_move
        :return: Whether the wall is horizontal, vertical, or the move is a piece_move
        """
        return self._is_horizontal

