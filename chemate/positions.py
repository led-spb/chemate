import functools
from abc import abstractmethod
from chemate.figure import FigureCreator
from chemate.utils import Position


class PositionFactory:
    @abstractmethod
    def figures(self):
        """
        :rtype: Iterator of Figure
        """
        pass


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
