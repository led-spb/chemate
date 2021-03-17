from chemate.utils import Position, Direction, Player
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

    def available_moves(self):
        """
        Get available moves for current figure position
        :return: Iterator for chemate.utils.Position object with valid positions of this figure
        """
        return None

    def move(self, new_position):
        """
        Moving figure to the new position
        :param new_position: Position
        """
        self.board.make_move(from_pos=self.position, to_pos=new_position)

    def generate_moves(self, direction, only_empty=False, limit=8):
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


class Pawn(Figure):
    def available_moves(self):
        # Pawn can move 1 (or 2 on first move) on forward
        in_initial_pos = self.position.y == (1 if self.color == Player.WHITE else 6)
        yield from self.generate_moves(
            direction=Direction.up if self.color == Player.WHITE else Direction.down,
            only_empty=True,
            limit=2 if in_initial_pos else 1
        )

        # Pawn can fight only 1 on forward diagonal
        moves = [self.position + (Direction.up_left if self.color == Player.WHITE else Direction.down_left),
                 self.position + (Direction.up_right if self.color == Player.WHITE else Direction.down_right)]
        for new in moves:
            if self.board.check_position(color=self.color, position=new) == 1:
                yield new
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
        for new in all_positions:
            check = self.board.check_position(color=self.color, position=new)
            if check <= 1:
                yield new
        pass

    @Figure.char.getter
    def char(self):
        return 'N' if self.color == Player.WHITE else 'n'


class Bishop(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 3

    def available_moves(self):
        yield from self.generate_moves(Direction.up_left)
        yield from self.generate_moves(Direction.up_right)
        yield from self.generate_moves(Direction.down_right)
        yield from self.generate_moves(Direction.down_left)

    @Figure.char.getter
    def char(self):
        return 'B' if self.color == Player.WHITE else 'b'


class Rook(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 5

    def available_moves(self):
        yield from self.generate_moves(Direction.up)
        yield from self.generate_moves(Direction.right)
        yield from self.generate_moves(Direction.down)
        yield from self.generate_moves(Direction.left)

    @Figure.char.getter
    def char(self):
        return 'R' if self.color == Player.WHITE else 'r'


class Queen(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 9

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
    def __init__(self, color, position):
        super().__init__(color, position)
        self._price = 90

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
