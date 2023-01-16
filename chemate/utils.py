class Direction(object):
    """
    This class describes directions for move
    """
    UP = 8
    DOWN = -8
    LEFT = -1
    RIGHT = 1
    UP_LEFT = 7
    UP_RIGHT = 9
    DOWN_LEFT = -9
    DOWN_RIGHT = -7


class Painter:
    def draw_board(self, board, **args):
        pass


class StringPainter(Painter):
    def draw_board(self, board, **args):
        lines = [['.' for x in range(8)] for y in range(8)]
        for figure in board.figures():
            lines[7-figure.position.y][figure.position.x] = figure.char

        return "\n".join([" ".join(line) for line in lines])
