
DIVIDER = "@"


class DrawTile:

    def __init__(self, coord, dim):
        self.coordinate = coord
        self.dimensions = dim
        self.tile_template = self.__get_tile_template()

    def __get_tile_template(self):
        from Display.DrawBoard import SYMBOLS

        row = self.coordinate.row
        col = self.coordinate.column
        dim = self.dimensions - 1

        if row == 0 and col == 0:
            return f"{SYMBOLS['tl_crn']}""{nh_wal}"f"{SYMBOLS['t_intr']}%s" \
                   "{wv_wal}{player}{ev_wal}%s" \
                   f"{SYMBOLS['l_intr']}""{sh_wal}"f"{SYMBOLS['m_intr']}%s" \
                   % (DIVIDER, DIVIDER, DIVIDER)
        elif row == 0 and 0 < col < dim:
            return "{nh_wal}"f"{SYMBOLS['t_intr']}%s" \
                   "{player}{ev_wal}%s" \
                   "{sh_wal}"f"{SYMBOLS['m_intr']}%s" \
                   % (DIVIDER, DIVIDER, DIVIDER)
        elif row == 0 and col == dim:
            return "{nh_wal}"f"{SYMBOLS['tr_crn']}\n%s" \
                   "{player}{ev_wal}\n%s" \
                   "{sh_wal}"f"{SYMBOLS['r_intr']}\n%s" \
                   % (DIVIDER, DIVIDER, DIVIDER)
        elif 0 < row and col == 0:
            bottom = ("bl_crn", "b_intr") if row == dim else ("l_intr", "m_intr")
            return "{wv_wal}{player}{ev_wal}%s" \
                   f"{SYMBOLS[bottom[0]]}""{sh_wal}"f"{SYMBOLS[bottom[1]]}%s" \
                   % (DIVIDER, DIVIDER)
        elif 0 < row and 0 < col < dim:
            bottom = "b_intr" if row == dim else "m_intr"
            return "{player}{ev_wal}%s" \
                   "{sh_wal}"f"{SYMBOLS[bottom]}%s" \
                   % (DIVIDER, DIVIDER)
        elif 0 < row and col == dim:
            bottom = "br_crn" if row == dim else "r_intr"
            return "{player}{ev_wal}\n%s" \
                   "{sh_wal}"f"{SYMBOLS[bottom]}\n%s" \
                   % (DIVIDER, DIVIDER)

    @staticmethod
    def __get_player(occupant):
        from Display.DrawBoard import DrawBoard

        return DrawBoard.get_players()[occupant]

    @staticmethod
    def __get_wall(neighbor, sym, h_wall):
        return \
            sym['bh_wall' if neighbor is None else 'h_wall'] if h_wall else \
            sym['bv_wall' if neighbor is None else 'v_wall']
