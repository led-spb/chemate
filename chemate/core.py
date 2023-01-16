from typing import Iterator

import chemate.figures


class Player(object):
    """
    Constants for determine player's side
    """
    WHITE = 1
    BLACK = -1


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
        y = int(value[1]) - 1
        return cls.from_xy(x, y)

    @classmethod
    def from_xy(cls, x, y):
        index = y * 8 + x
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
        return "%s%d" % (chr(ord('a') + self.x), self.y + 1)

    def __eq__(self, other):
        return self.index == other.index


class Direction:
    delta = 0
    all_positions = [Position(index) for index in range(64)]

    def __init__(self, position: Position, limit: int = 7) -> None:
        self.position = position
        self.limit = limit

    def __iter__(self):
        return self

    def stop_iterate(self) -> bool:
        return self.limit == 0

    def __next__(self) -> Position:
        if self.stop_iterate():
            raise StopIteration()
        self.position = self.all_positions[self.position.index + self.delta]
        self.limit -= 1
        return self.position


class Movement(object):
    __slots__ = ["figure",
                 "from_pos",
                 "to_pos",
                 "taken_figure",
                 "rook",
                 "transform_to",
                 "is_check",
                 "is_mate",
                 ]

    """
    This class describes one movement on the board
    """

    def __init__(self,
                 figure=None,
                 from_pos=None,
                 to_pos=None,
                 taken_figure=None,
                 rook=None,
                 transform_to=None) -> None:
        self.figure = figure
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.rook = rook
        self.transform_to = transform_to
        self.taken_figure = taken_figure
        self.is_check = False
        self.is_mate = False

    @classmethod
    def from_char(cls, data):
        pos = data.split('-')
        return cls(from_pos=Position.from_char(pos[0]), to_pos=Position.from_char(pos[1]))

    def __str__(self):
        if self.rook is not None:
            return '0-0-0' if self.to_pos.index-self.from_pos.index < 0 else '0-0'
        return "%s%s%s%s%s" % (
            '' if isinstance(self.figure, chemate.figures.Pawn) else self.figure.char,
            str(self.from_pos),
            '-' if self.taken_figure is None else 'x',
            str(self.to_pos),
            '+' if self.is_check else ''
        )


class Figure:
    _price = 0
    _char = '.'
    _char_maps = dict(zip("KQRBNPkqrbnp", (chr(uc) for uc in range(0x2654, 0x2660))))

    def __init__(self, color: int, position: Position):
        self.color = color
        self.position = position
        self.moves = 0
        pass

    def copy(self):
        """
        Create exact copy of current figure
        :return: cloned Figure
        """
        return self.__class__(self.color, self.position)

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.color == other.color \
               and self.position == other.position

    @property
    def price(self) -> int:
        return self.color * self._price

    @property
    def has_moved(self):
        return self.moves > 0

    @property
    def char(self):
        return self._char.upper() if self.color == Player.WHITE else self._char.lower()

    @property
    def unicode_char(self):
        return Figure._char_maps[self.char]

    def __str__(self):
        return f'{self.char}{self.position}'

    def directions(self, attack: bool = False) -> Iterator[Direction]:
        pass
