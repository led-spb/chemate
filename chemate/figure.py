from chemate.utils import Position, Direction
from chemate.player import Player
import itertools


class Figure(object):
    def __init__(self, color, position):
        self.color = color
        self.board = None
        self.position = position
        # self.initial_position = position.copy()
        self.initial_position = Position(position.x, position.y)

    @property
    def char(self):
        return ' '

    @property
    def is_moved(self):
        return self.position != self.initial_position

    def __eq__(self, other):
        return self.__class__ == other.__class__ \
               and self.color == other.color \
               and self.position == other.position

    def copy(self):
        """
        Create exact copy of current figure
        :return:
        """
        return self.__class__(self.color, self.position)

    def available_moves(self):
        """
        Get available moves for current figure position
        :return: iterator with valid positions of this figure
        """
        return None

    def move(self, new_position):
        """
        Moving figure to the new position
        :param new_position:
        :return: None
        """
        self.board.make_move(from_pos=self.position, to_pos=new_position)

    def generate_moves(self, direction, only_empty=False, limit=8):
        """
        Generate continues moves in direction from current position
        :param direction:
        :param only_empty:
        :param limit:
        :return: Iterator object with available positions
        """
        position = Position(self.position.x, self.position.y)
        for i in itertools.count():
            if i >= limit:
                break
            position = position + direction
            check = self.board.check_position(color=self.color, position=position)
            if check >= 0 and check != 1 and (not only_empty or check == 0):
                yield position
                if check == 2:
                    break
            else:
                break
        pass


class Pawn(Figure):
    def available_moves(self):
        # Pawn can move 1 (or 2 on first move) on forward
        yield from self.generate_moves(
            direction=Direction.up if self.color == Player.WHITE else Direction.down,
            only_empty=True,
            limit=1 if self.is_moved else 2
        )

        # Pawn can fight only 1 on forward diagonal
        moves = [self.position + (Direction.up_left if self.color == Player.WHITE else Direction.down_left),
                 self.position + (Direction.up_right if self.color == Player.WHITE else Direction.down_right)]
        for new in moves:
            if self.board.check_position(color=self.color, position=new) == 2:
                yield new
        pass

    @Figure.char.getter
    def char(self):
        return 'P' if self.color == Player.WHITE else 'p'


class Knight(Figure):
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
        for new in all_positions:
            check = self.board.check_position(color=self.color, position=new)
            if check >= 0 and check > 1:
                yield new
        pass

    @Figure.char.getter
    def char(self):
        return 'N' if self.color == Player.WHITE else 'n'


class Bishop(Figure):
    def available_moves(self):
        yield from self.generate_moves(Direction.up_left)
        yield from self.generate_moves(Direction.up_right)
        yield from self.generate_moves(Direction.down_right)
        yield from self.generate_moves(Direction.down_left)

    @Figure.char.getter
    def char(self):
        return 'B' if self.color == Player.WHITE else 'b'


class Rook(Figure):
    def available_moves(self):
        yield from self.generate_moves(Direction.up)
        yield from self.generate_moves(Direction.right)
        yield from self.generate_moves(Direction.down)
        yield from self.generate_moves(Direction.left)

    @Figure.char.getter
    def char(self):
        return 'R' if self.color == Player.WHITE else 'r'


class Queen(Figure):
    def available_moves(self):
        yield from self.generate_moves(Direction.up_left)
        yield from self.generate_moves(Direction.up_right)
        yield from self.generate_moves(Direction.down_right)
        yield from self.generate_moves(Direction.down_left)
        yield from self.generate_moves(Direction.up)
        yield from self.generate_moves(Direction.right)
        yield from self.generate_moves(Direction.down)
        yield from self.generate_moves(Direction.left)

    @Figure.char.getter
    def char(self):
        return 'Q' if self.color == Player.WHITE else 'q'


class King(Figure):
    def available_moves(self):
        yield from self.generate_moves(Direction.up_left, limit=1)
        yield from self.generate_moves(Direction.up_right, limit=1)
        yield from self.generate_moves(Direction.down_right, limit=1)
        yield from self.generate_moves(Direction.down_left, limit=1)
        yield from self.generate_moves(Direction.up, limit=1)
        yield from self.generate_moves(Direction.right, limit=1)
        yield from self.generate_moves(Direction.down, limit=1)
        yield from self.generate_moves(Direction.left, limit=1)

    @Figure.char.getter
    def char(self):
        return 'K' if self.color == Player.WHITE else 'k'
