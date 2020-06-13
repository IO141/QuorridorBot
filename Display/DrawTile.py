
DIVIDER = "@"


class DrawTile:

    def __init__(self, coord, dim):
        self.coordinate = coord
        self.dimensions = dim
        self.tile_template = self.__get_tile_template()

    def __get_tile_template(self):
        row = self.coordinate.row
        col = self.coordinate.column
        dim = self.dimensions - 1

        if row == 0 and col == 0:
            return "%s%s%s{0}" \
                   "%s%s%s{0}" \
                   "%s%s%s{0}".format(DIVIDER)
        elif row == 0 and 0 < col < dim:
            return "%s%s{0}" \
                   "%s%s{0}" \
                   "%s%s{0}".format(DIVIDER)
        elif row == 0 and col == dim:
            return "%s%s\n{0}" \
                   "%s%s\n{0}" \
                   "%s%s\n{0}".format(DIVIDER)
        elif 0 < row and col == 0:
            return "%s%s%s{0}" \
                   "%s%s%s{0}".format(DIVIDER)
        elif 0 < row and 0 < col < dim:
            return "%s%s{0}" \
                   "%s%s{0}".format(DIVIDER)
        elif 0 < row and col == dim:
            return "%s%s\n{0}" \
                   "%s%s\n{0}".format(DIVIDER)

    def gen(self):
        return self.coordinate

    def draw(self):
        row = self.coordinate.row
        col = self.coordinate.column
        dim = self.dimensions

        # b == border, w == wall, i == intersection (with wall)
        if row == 0 and col == 0:
            # top left corner, eval NORTH-b + WEST-b + SOUTH-i + EAST-w
            # %s%s%s \n %s%s%s \n %s%s%s
            pass
        if row == 0 and 0 < col < dim:
            # top side, eval NORTH-b + SOUTH-i + EAST-w
            # %s%s \n %s%s \n %s%s
            pass
        if row == 0 and col == dim:
            # top right corner, eval NORTH-b + SOUTH-w + EAST-b
            # %s%s \n %s%s \n %s%s
            pass
        if 0 < row < dim and col == 0:
            # left side, eval WEST-b + SOUTH-i + EAST-w
            # %s%s%s \n %s%s%s
            pass
        if 0 < row < dim and 0 < col < dim:
            # mid block, eval SOUTH-i + EAST-w
            # %s%s \n %s%s
            pass
        if 0 < row < dim and col == dim:
            # right side, eval SOUTH-w + EAST-b
            # %s%s \n %s%s
            pass
        if row == dim and col == 0:
            # bottom left corner, eval WEST-b + SOUTH-b + EAST-w
            # %s%s%s \n %s%s%s
            pass
        if row == dim and 0 < col < dim:
            # bottom side, eval SOUTH-b + EAST-w
            # %s%s \n %s%s
            pass
        if row == dim and col == dim:
            # bottom right corner, eval SOUTH-b + EAST-b
            # %s%s \n %s%s
            pass
