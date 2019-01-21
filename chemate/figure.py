from chemate.utils import Position, Direction
from chemate.player import Player
import itertools


class Figure(object):
    def __init__(self, color, position):
        self.color = color
        self.board = None
        self.position = position

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
        if new_position in self.available_moves():
            self.position = new_position.copy()

    def generate_moves(self, direction, only_empty=False, limit=8):
        """
        Generate continues moves in direction from current position
        :param direction:
        :param only_empty:
        :param limit:
        :return: Iterator object with available positions
        """
        position = self.position.copy()
        for i in itertools.count():
            position = position + direction
            if i < limit and self.board.can_move(color=self.color, position=position, only_empty=only_empty):
                yield position
            else:
                break
        pass


class Pawn(Figure):
    def __init__(self, color, position):
        super().__init__(color, position)
        self.initial_position = position.copy()

    def available_moves(self):
        # Pawn can move 1 (or 2 on first move) on forward
        yield from self.generate_moves(
            direction=Direction.up if self.color == Player.WHITE else Direction.down,
            only_empty=True,
            limit=2 if self.position == self.initial_position else 1
        )

        # Pawn can fight only 1 on forward diagonal
        moves = [self.position + (Direction.up_left if self.color == Player.WHITE else Direction.down_left),
                 self.position + (Direction.up_right if self.color == Player.WHITE else Direction.down_right)]
        for new in moves:
            if self.board.can_move(color=self.color, position=new, only_opposite=True):
                yield new
        pass


class Horse(Figure):
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
            if self.board.can_move(color=self.color, position=new):
                yield new
        pass


class Elephant(Figure):
    def available_moves(self):
        yield from self.generate_moves(Direction.up_left)
        yield from self.generate_moves(Direction.up_right)
        yield from self.generate_moves(Direction.down_right)
        yield from self.generate_moves(Direction.down_left)


class Tower(Figure):
    def available_moves(self):
        yield from self.generate_moves(Direction.up)
        yield from self.generate_moves(Direction.right)
        yield from self.generate_moves(Direction.down)
        yield from self.generate_moves(Direction.left)


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
