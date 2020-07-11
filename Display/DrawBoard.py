from re import sub
from colorama import Fore, Back, Style, init
from Display.DrawTile import DrawTile, DIVIDER

init(autoreset=True)

PLAYER = "●"

BG = Back.LIGHTWHITE_EX + Style.NORMAL
STD = BG + Fore.BLACK
BLANK = BG + Fore.LIGHTWHITE_EX
RST = Style.RESET_ALL

SYMBOLS = {
    "t_intr": STD + "┬" + RST, "b_intr": STD + "┴" + RST, "l_intr": STD + "├" + RST,
    "r_intr": STD + "┤" + RST, "m_intr": STD + "┼" + RST, "tl_crn": STD + "┌" + RST,
    "tr_crn": STD + "┐" + RST, "bl_crn": STD + "└" + RST, "br_crn": STD + "┘" + RST,
    "h_wall": STD + "───" + RST, "v_wall": STD + "│" + RST,
    "bh_wall": BLANK + "───" + RST, "bv_wall": BLANK + "│" + RST
}


class DrawBoard:

    def __init__(self, board):
        self.__board = board
        self.dim = board.dimensions
        self.board_template = self._get_board_template()

    def _get_board_template(self):
        board_template = self.__get_board_template()

        for i in range(self.dim):
            for j in range(self.dim):
                board_template[i][j] %= DrawTile(self.__board.board[i][j], self.dim)
        return board_template

    def __get_board_template(self):
        return [["%s" for _ in range(self.dim)] for _ in range(self.dim)]

    def _board_template_to_string(self):
        pint = ""
        for row in self.board_template:
            for col in row:
                pint += sub("[@\n]", "", col)
            pint += "\n"
        return pint

    def format_template(self):
        board_3d = [[i.split(DIVIDER) for i in self.board_template[j]] for j in range(len(self.board_template))]
        pint = ""
        for i in range(self.dim):
            row = [list(j) for j in zip(*board_3d[i])]
            pint += "".join("".join(k) for k in row)
        return pint

    @staticmethod
    def get_players():
        player = BG + PLAYER
        space = BG + " "

        return [
            (space, Fore.RED + player, space),      # Player 1
            (space, Fore.GREEN + player, space),    # Player 2
            (space, Fore.YELLOW + player, space),   # Player 3
            (space, Fore.BLUE + player, space),     # Player 4
            (space, Fore.BLACK + player, space)     # No player
        ]
