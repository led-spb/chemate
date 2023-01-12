import chemate.figure


class Position(object):
    """
    This class describes figure position at board
    """
    __slots__ = ['index']

    def __init__(self, index):
        self.index = index

    @classmethod
    def from_char(cls, value):
        x = ord(value.lower()[0]) - ord('a')
        y = int(value[1])-1
        return cls.from_xy(x, y)

    @classmethod
    def from_xy(cls, x, y):
        index = y*8+x
        return cls(index)

    def is_last_line_for(self, color):
        return (self.y == 7 and color == Player.WHITE) or (self.y == 0 and color == Player.BLACK)

    @property
    def color(self):
        return Player.WHITE if (self.index + self.y % 2) % 2 else Player.BLACK

    @property
    def x(self):
        return self.index % 8

    @property
    def y(self):
        return self.index // 8

    def __add__(self, other):
        return Position(self.index + other)

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
    UP = 8
    DOWN = -8
    LEFT = -1
    RIGHT = 1
    UP_LEFT = 7
    UP_RIGHT = 9
    DOWN_LEFT = -9
    DOWN_RIGHT = -7


class Player(object):
    """
    Constants for determine player's side
    """
    WHITE = 1
    BLACK = -1


class Movement(object):
    __slots__ = ["figure", "from_pos", "to_pos", "taken_figure", "rook", "transform_to", "is_check", "is_passthrough"]

    """
    This class describes one movement on board
    """
    def __init__(self,
                 figure=None,
                 from_pos=None,
                 to_pos=None,
                 taken_figure=None,
                 rook=None,
                 transform_to=None,
                 is_passthrough=False) -> None:
        self.figure = figure
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.rook = rook
        self.transform_to = transform_to
        self.taken_figure = taken_figure
        self.is_check = False
        self.is_passthrough = is_passthrough

    @classmethod
    def from_char(cls, data):
        pos = data.split('-')
        return cls(from_pos=Position.from_char(pos[0]), to_pos=Position.from_char(pos[1]))

    def __str__(self):
        if self.rook is not None:
            return '0-0-0' if self.rook.position.x == 0 else '0-0'
        return "%s%s%s%s%s" % (
            '' if isinstance(self.figure, chemate.figure.Pawn) else self.figure.char.upper(),
            str(self.from_pos),
            '-' if self.taken_figure is None else 'x',
            str(self.to_pos),
            '+' if self.is_check else ''
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
