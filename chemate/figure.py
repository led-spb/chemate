import functools
from typing import Iterator, List

from chemate.utils import Position, Direction, Player, Movement
import itertools


class Figure(object):
    _char_maps = dict(zip("KQRBNPkqrbnp", (chr(uc) for uc in range(0x2654, 0x2660))))

    def __init__(self, color, position):
        self.color = color
        self.board = None
        self.position = position
        self._price = 1

    @property
    def char(self):
        return '.'

    def __str__(self):
        return self.char+self.position

    @property
    def unicode_char(self):
        return Figure._char_maps[self.char]

    @property
    def price(self):
        return self._price * self.color

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.color == other.color \
               and self.position == other.position

    def copy(self):
        """
        Create exact copy of current figure
        :return: cloned Figure
        """
        return self.__class__(self.color, self.position)

    def available_moves(self) -> Iterator[Movement]:
        """
        Get available moves for current figure position
        :return: Iterator for chemate.utils.Position object with valid positions of this figure
        """
        pass

    def move(self, new_position):
        """
        Moving figure to the new position
        :param new_position: Position
        """
        self.board.make_move(Movement(from_pos=self.position, to_pos=new_position))


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


class Pawn(Figure):
    def _gen_replace_figures(self):
        return [Queen(self.color, None), Rook(self.color, None), Knight(self.color, None), Bishop(self.color, None)]

    def available_moves(self):
        # Pawn can move 1 (or 2 on first move) on forward
        direction = Direction.UP if self.color == Player.WHITE else Direction.DOWN
        limit = 2 if self.position.y == (1 if self.color == Player.WHITE else 6) else 1

        for new_pos in self.board.gen_positions_by_dir(self.position, direction, color=None, limit=limit):
            # Transformation on last line
            if new_pos.is_last_line_for(self.color):
                for new_figure in self._gen_replace_figures():
                    yield Movement(self, self.position, new_pos, transform_to=new_figure)
            else:
                yield Movement(self, self.position, new_pos)

        # Pawn can fight only 1 on forward diagonal
        all_pos = list(
            itertools.chain(
                self.board.gen_positions_by_dir(
                    self.position,
                    Direction.UP_LEFT if self.color == Player.WHITE else Direction.DOWN_LEFT,
                    color=self.color, limit=1
                ),
                self.board.gen_positions_by_dir(
                    self.position,
                    Direction.UP_RIGHT if self.color == Player.WHITE else Direction.DOWN_RIGHT,
                    color=self.color, limit=1))
        )

        for new_pos in all_pos:
            if self.board.get_figure(new_pos) is None:
                continue
            if new_pos.is_last_line_for(self.color):
                for new_figure in self._gen_replace_figures():
                    yield Movement(self, self.position, new_pos, transform_to=new_figure)
            else:
                yield Movement(self, self.position, new_pos)
        pass

    @Figure.char.getter
    def char(self):
        return 'P' if self.color == Player.WHITE else 'p'


class Knight(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 3

    def available_moves(self):
        all_positions = [
            (self.position.x+1, self.position.y+2),
            (self.position.x+2, self.position.y+1),
            (self.position.x+2, self.position.y-1),
            (self.position.x+1, self.position.y-2),
            (self.position.x-1, self.position.y-2),
            (self.position.x-2, self.position.y-1),
            (self.position.x-2, self.position.y+1),
            (self.position.x-1, self.position.y+2)
        ]
        for x, y in all_positions:
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            new_pos = Position.from_xy(x, y)
            figure = self.board.get_figure(new_pos)
            if figure is None or figure.color != self.color:
                yield Movement(self, self.position, new_pos)
        pass

    @Figure.char.getter
    def char(self):
        return 'N' if self.color == Player.WHITE else 'n'


class Bishop(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 3

    def available_moves(self):
        for new_pos in itertools.chain(
               self.board.gen_positions_by_dir(self.position, Direction.UP_LEFT, self.color),
               self.board.gen_positions_by_dir(self.position, Direction.UP_RIGHT, self.color),
               self.board.gen_positions_by_dir(self.position, Direction.DOWN_LEFT, self.color),
               self.board.gen_positions_by_dir(self.position, Direction.DOWN_RIGHT, self.color)):
            yield Movement(self, self.position, new_pos)

    @Figure.char.getter
    def char(self):
        return 'B' if self.color == Player.WHITE else 'b'


class Rook(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 5

    def available_moves(self):
        for new_pos in itertools.chain(
                self.board.gen_positions_by_dir(self.position, Direction.UP, self.color),
                self.board.gen_positions_by_dir(self.position, Direction.RIGHT, self.color),
                self.board.gen_positions_by_dir(self.position, Direction.DOWN, self.color),
                self.board.gen_positions_by_dir(self.position, Direction.LEFT, self.color)):
            yield Movement(self, self.position, new_pos)

    @Figure.char.getter
    def char(self):
        return 'R' if self.color == Player.WHITE else 'r'


class Queen(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 9

    def available_moves(self):
        for new_pos in itertools.chain(
                self.board.gen_positions_by_dir(self.position, Direction.UP_LEFT, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.UP_RIGHT, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.DOWN_RIGHT, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.DOWN_LEFT, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.UP, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.RIGHT, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.DOWN, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.LEFT, color=self.color)):
            yield Movement(self, self.position, new_pos)

    @Figure.char.getter
    def char(self):
        return 'Q' if self.color == Player.WHITE else 'q'


class King(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.home_position = Position.from_char('e1') if self.color == Player.WHITE else Position.from_char('e8')
        self._price = 90

    def available_moves(self):
        for new_pos in itertools.chain(
                self.board.gen_positions_by_dir(self.position, Direction.UP_LEFT, limit=1, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.UP_RIGHT, limit=1, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.DOWN_RIGHT, limit=1, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.DOWN_LEFT, limit=1, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.UP, limit=1, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.RIGHT, limit=1, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.DOWN, limit=1, color=self.color),
                self.board.gen_positions_by_dir(self.position, Direction.LEFT, limit=1, color=self.color)):
            yield Movement(self, self.position, new_pos)

        # Unable to rook when king already moved or has check
        if self.position != self.home_position or self.board.has_moved(self):
            return

        yield from self.rook_moves(False)
        yield from self.rook_moves(True)
        pass

    @Figure.char.getter
    def char(self):
        return 'K' if self.color == Player.WHITE else 'k'

    def rook_moves(self, long):
        # unable to rook is between figures hasn't empty cells
        for i in range(-1 if long else 1, -4 if long else 3, -1 if long else 1):
            check_pos = Position(self.position.index + i)
            if self.board.get_figure(check_pos) is not None:
                return

        rook = self.board.get_figure(Position.from_xy(0 if long else 7, self.position.y))
        # Unable to rook when rook already moved
        if rook is None or not isinstance(rook, Rook) or rook.color != self.color or self.board.has_moved(rook):
            return
        check_pos = Position(self.position.index + (-2 if long else 2))
        yield Movement(figure=self, from_pos=self.position, to_pos=check_pos, rook=rook)
