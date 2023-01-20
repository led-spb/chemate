import functools
from abc import abstractmethod
from typing import Iterator

from chemate.figures import Rook, Bishop, Knight, King, Queen, Pawn
from chemate.core import Position, Player, Figure


class PositionFactory:
    def apply(self, board):
        board.clear()
        board.put_figures(self.figures())
        board.current = Player.WHITE

    @abstractmethod
    def figures(self) -> Iterator[Figure]:
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
        portion = iter(data.split(' '))
        self.figure_data = next(portion)
        self.current = next(portion, 'w')
        self.rooking = next(portion, 'RQrq')
        self.passthru = next(portion, '-')
        self.empty_moves = next(portion, '0')
        self.move_no = next(portion, '1')
        pass

    def apply(self, board):
        super().apply(board)
        board.current = Player.WHITE if self.current.lower() == 'w' else Player.BLACK
        board.move_number = int(self.move_no)
        if self.rooking[0] == '-':
            self.disable_rooking(board, Position.from_char('h1'), Player.WHITE)
        if self.rooking[1] == '-':
            self.disable_rooking(board, Position.from_char('a1'), Player.WHITE)
        if self.rooking[2] == '-':
            self.disable_rooking(board, Position.from_char('h8'), Player.BLACK)
        if self.rooking[3] == '-':
            self.disable_rooking(board, Position.from_char('a8'), Player.BLACK)
        pass

    @staticmethod
    def disable_rooking(board, pos: Position, color: int):
        fig = board.figure_at(pos)
        if fig is not None and fig.color == color:
            fig.moves += 1

    def figures(self):
        x, y = 0, 7
        for chr in self.figure_data:
            if chr == '/':
                x, y = 0, y - 1
                continue
            if chr.isdigit():
                x += int(chr)
                continue
            yield FigureCreator.by_char(chr)(Position.from_xy(x, y))
            x = x + 1
        yield from ()


InitialPosition = functools.partial(PredefinedFENPosition, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w RQrq - 0 1')
