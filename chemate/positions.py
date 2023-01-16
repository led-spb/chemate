import functools
from abc import abstractmethod

from chemate.figures import Rook, Bishop, Knight, King, Queen, Pawn
from chemate.core import Position, Player


class PositionFactory:
    @abstractmethod
    def figures(self):
        """
        :rtype: Iterator of Figure
        """
        pass


class FigureCreator:
    @staticmethod
    def by_char(char):
        color = Player.WHITE if char.isupper() else Player.BLACK
        if char in ('r', 'R'):
            return functools.partial(Rook, color)
        if char in ('b', 'B'):
            return functools.partial(Bishop, color)
        if char in ('n', 'N'):
            return functools.partial(Knight, color)
        if char in ('k', 'K'):
            return functools.partial(King, color)
        if char in ('q', 'Q'):
            return functools.partial(Queen, color)
        if char in ('p', 'P'):
            return functools.partial(Pawn, color)
        raise RuntimeError('Unknown figure "%s"' % char)


class EmptyPosition(PositionFactory):
    def figures(self):
        yield from ()


class PredefinedFENPosition(PositionFactory):
    def __init__(self, data):
        self.curr_y = 7
        self.curr_x = 0
        self.data = data.split(' ')[0]
        pass

    def figures(self):
        x, y = 0, 7
        for chr in self.data:
            if chr == '/':
                x, y = 0, y - 1
                continue
            if chr.isdigit():
                x += int(chr)
                continue
            yield FigureCreator.by_char(chr)(Position.from_xy(x, y))
            x = x + 1
        yield from ()


InitialPosition = functools.partial(PredefinedFENPosition, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
