import functools
from typing import Iterator

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

    def gen_position_by_moves(self, direction, only_empty=False, limit=8):
        """
        Generate continues moves in direction from current position
        :param direction: Direction
        :param only_empty: Generate new posiotion if cell is empty only
        :param limit: Check only first moves in this direction
        :return: Iterator for Position object with available positions
        """
        position = Position(self.position.x, self.position.y)
        for i in itertools.count():
            if i >= limit:
                break
            position = position + direction
            check = self.board.check_position(color=self.color, position=position)
            if check <= 1 and (not only_empty or check == 0):
                yield position
                if check == 1:
                    break
            else:
                break
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


class Pawn(Figure):
    def _gen_replace_figures(self):
        return [Queen(self.color, None), Rook(self.color, None), Knight(self.color, None), Bishop(self.color, None)]

    def available_moves(self):
        # Pawn can move 1 (or 2 on first move) on forward
        in_initial_pos = self.position.y == (1 if self.color == Player.WHITE else 6)
        for new_pos in self.gen_position_by_moves(
                            direction=Direction.up if self.color == Player.WHITE else Direction.down,
                            only_empty=True, limit=2 if in_initial_pos else 1):
            # Transformation on last line
            if new_pos.is_last_line_for(self.color):
                for new_figure in self._gen_replace_figures():
                    yield Movement(self, self.position, new_pos, transform_to=new_figure)
            else:
                yield Movement(self, self.position, new_pos)

        # Pawn can fight only 1 on forward diagonal
        positions = [self.position + (Direction.up_left if self.color == Player.WHITE else Direction.down_left),
                     self.position + (Direction.up_right if self.color == Player.WHITE else Direction.down_right)]
        for new_pos in positions:
            if self.board.check_position(color=self.color, position=new_pos) == 1:
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
            Position(self.position.x+1, self.position.y+2),
            Position(self.position.x+2, self.position.y+1),
            Position(self.position.x+2, self.position.y-1),
            Position(self.position.x+1, self.position.y-2),

            Position(self.position.x-1, self.position.y-2),
            Position(self.position.x-2, self.position.y-1),
            Position(self.position.x-2, self.position.y+1),
            Position(self.position.x-1, self.position.y+2)
        ]
        for new_pos in all_positions:
            check = self.board.check_position(color=self.color, position=new_pos)
            if check <= 1:
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
        for new_pos in itertools.chain(self.gen_position_by_moves(Direction.up_left),
                                       self.gen_position_by_moves(Direction.up_right),
                                       self.gen_position_by_moves(Direction.down_right),
                                       self.gen_position_by_moves(Direction.down_left)):
            yield Movement(self, self.position, new_pos)

    @Figure.char.getter
    def char(self):
        return 'B' if self.color == Player.WHITE else 'b'


class Rook(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 5

    def available_moves(self):
        for new_pos in itertools.chain(self.gen_position_by_moves(Direction.up),
                                       self.gen_position_by_moves(Direction.right),
                                       self.gen_position_by_moves(Direction.down),
                                       self.gen_position_by_moves(Direction.left)):
            yield Movement(self, self.position, new_pos)

    @Figure.char.getter
    def char(self):
        return 'R' if self.color == Player.WHITE else 'r'


class Queen(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 9

    def available_moves(self):
        for new_pos in itertools.chain(self.gen_position_by_moves(Direction.up_left),
                                       self.gen_position_by_moves(Direction.up_right),
                                       self.gen_position_by_moves(Direction.down_right),
                                       self.gen_position_by_moves(Direction.down_left),
                                       self.gen_position_by_moves(Direction.up),
                                       self.gen_position_by_moves(Direction.right),
                                       self.gen_position_by_moves(Direction.down),
                                       self.gen_position_by_moves(Direction.left)):
            yield Movement(self, self.position, new_pos)

    @Figure.char.getter
    def char(self):
        return 'Q' if self.color == Player.WHITE else 'q'


class King(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 90

    def available_moves(self):
        for new_pos in itertools.chain(self.gen_position_by_moves(Direction.up_left, limit=1),
                                       self.gen_position_by_moves(Direction.up_right, limit=1),
                                       self.gen_position_by_moves(Direction.down_right, limit=1),
                                       self.gen_position_by_moves(Direction.down_left, limit=1),
                                       self.gen_position_by_moves(Direction.up, limit=1),
                                       self.gen_position_by_moves(Direction.right, limit=1),
                                       self.gen_position_by_moves(Direction.down, limit=1),
                                       self.gen_position_by_moves(Direction.left, limit=1)):
            yield Movement(self, self.position, new_pos)
        # TODO: make rook movement

    @Figure.char.getter
    def char(self):
        return 'K' if self.color == Player.WHITE else 'k'

    def rook_moves(self, long):
        # Unable to rook when king already moved
        if self.board.has_moved(self):
            return

        if long:
            empty_pos = [
                Position(self.position.x - 1, self.position.y),
                Position(self.position.x - 2, self.position.y),
                Position(self.position.x - 3, self.position.y),
            ]
        else:
            empty_pos = [
                Position(self.position.x + 1, self.position.y),
                Position(self.position.x + 2, self.position.y),
            ]
        for p in empty_pos:
            if self.board.get_figure(p):
                return

        p = Position(0 if long else 7, self.position.y)
        rook = self.board.get_figure(p)

        # Unable to rook when rook already moved
        if rook is None or not isinstance(rook, Rook) or rook.color != self.color or self.board.has_moved(rook):
            return

        # Unable to rook then check
        if self.board.has_check(self.color):
            return
        pass
