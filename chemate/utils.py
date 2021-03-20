from collections import namedtuple
import chemate.figure


class Position(object):
    """
    This class describes figure position at board
    """
    __slots__ = ['x', 'y']

    def __init__(self, *args):
        if type(args[0]) == str:
            value = args[0]
            x = ord(value.lower()[0]) - ord('a')
            y = int(value[1]) - 1
        else:
            x = args[0]
            y = args[1]
        self.x = x
        self.y = y

    @classmethod
    def char(cls, value):
        x = ord(value.lower()[0]) - ord('a')
        y = int(value[1])-1
        return cls(x, y)

    @property
    def index(self):
        """
        Returns index in flat array
        :return: int
        """
        return self.y*8 + self.x

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __str__(self):
        """
        String representation of position
        :return:
        """
        return "%s%d" % (chr(ord('a') + self.x), self.y+1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Direction(object):
    """
    This class describes directions for move
    """
    up = Position(0, 1)
    down = Position(0, -1)
    left = Position(-1, 0)
    right = Position(1, 0)

    up_left = Position(-1, 1)
    up_right = Position(1, 1)
    down_left = Position(-1, -1)
    down_right = Position(1, -1)


class Player(object):
    """
    Constants for determine player's side
    """
    WHITE = 1
    BLACK = -1


BaseMovement = namedtuple('BaseMovement', ['figure', 'from_pos', 'to_pos', 'taken_figure', 'is_rook'])


class Movement(BaseMovement):
    """
    This class describes one movement on board
    """
    def __str__(self):
        return "%s%s%s%s" % (
            '' if isinstance(self.figure, chemate.figure.Pawn) else self.figure.char.upper(),
            str(self.from_pos),
            '-' if self.taken_figure is None else 'x',
            str(self.to_pos)
        )


class Painter:
    def draw_board(self, board, **args):
        pass


class StringPainter(Painter):
    def draw_board(self, board, **args):
        lines = [['.' for x in range(8)] for y in range(8)]
        for figure in board.figures():
            lines[7-figure.position.y][figure.position.x] = figure.char

        return "\n".join([" ".join(line) for line in lines])
