from chemate.figure import Pawn, Rook, Knight, Bishop, Queen, King
from chemate.player import Player
from chemate.utils import Position
from collections import namedtuple


BaseMovement = namedtuple('BaseMovement', ['figure', 'from_pos', 'to_pos', 'taken_figure'])


class Movement(BaseMovement):
    def __str__(self):
        return "%s%s%s%s" % (
            '' if isinstance(self.figure, Pawn) else self.figure.char.upper(),
            str(self.from_pos),
            '-' if self.taken_figure is None else 'x',
            str(self.to_pos)
        )


class Board(object):
    def __init__(self):
        self.board = None
        self.clear()
        self.moves = []
        self.balance = 0
        pass

    def __str__(self):
        """
        Current state of the board for debug
        :return: None
        """
        d = ["." if self.board[i] is None else self.board[i].char for i in range(64)]
        formatted = [" ".join(d[i-7:i+1]) for i in list(reversed(range(64)))[::8]]
        return "\n".join(formatted)

    def __hash__(self):
        """
        Calculates hash for current position
        :return:
        """
        return 0

    def clear(self):
        """
        Clears the board
        :return: None
        """
        self.board = [None for x in range(64)]

    def initial_position(self):
        """
        Generate initial state of board
        :return: None
        """
        self.board = [None for x in range(64)]
        self.put_figures(self.default_figures(Player.WHITE))
        self.put_figures(self.default_figures(Player.BLACK))

    @staticmethod
    def default_figures(color):
        """
        Generate all figures of specified color in default positions
        :param color: Color of the figures
        :return: Iterator for Figure instances
        """
        # Pawns
        for x in range(0, 8, 1):
            yield Pawn(color, Position(x, 1 if color == Player.WHITE else 6))
        # Towers
        for x in range(0, 8, 7):
            yield Rook(color, Position(x, 0 if color == Player.WHITE else 7))
        # Horses
        for x in range(1, 7, 5):
            yield Knight(color, Position(x, 0 if color == Player.WHITE else 7))
        # Elephants
        for x in range(2, 6, 3):
            yield Bishop(color, Position(x, 0 if color == Player.WHITE else 7))
        # Queen
        yield Queen(color, Position(3, 0 if color == Player.WHITE else 7))
        # King
        yield King(color, Position(4, 0 if color == Player.WHITE else 7))
        pass

    def put_figure(self, figure):
        """
        Put a figure on the board
        :return: None
        """
        self.board[figure.position.y*8 + figure.position.x] = figure
        figure.board = self
        self.balance += figure.price
        pass

    def get_figure(self, position):
        """
        Get figure at specified location on board
        :param position: Position on board
        :return: Figure instance or None
        """
        return self.board[position.index]

    def make_move(self, from_pos, to_pos):
        """
        Move figure to the new location
        :param from_pos:
        :param to_pos:
        :return: None
        """
        figure = self.board[from_pos.index]
        taken = self.board[to_pos.index]
        if taken is not None:
            self.balance -= taken.price

        self.moves.append(
            Movement(
                figure=figure,
                from_pos=from_pos,
                to_pos=to_pos,
                taken_figure=taken
            )
        )
        self.board[from_pos.index] = None
        self.board[to_pos.index] = figure
        figure.position = to_pos

    def rollback_move(self):
        last_move = self.moves.pop()
        self.board[last_move.from_pos.index] = last_move.figure
        self.board[last_move.to_pos.index] = last_move.taken_figure
        last_move.figure.position = last_move.from_pos
        if last_move.taken_figure is not None:
            self.balance += last_move.taken_figure.price

    def put_figures(self, it):
        """
        Put all figures on the board from iterator
        :param it:
        :return: None
        """
        list(map(self.put_figure, it))

    def figures(self):
        """
        Get all figures on the board
        :return: Iterator object with all figures
        """
        for figure in self.board:
            if figure is not None:
                yield figure
        pass

    def check_position(self, color, position):
        """
        Check specified position
        :param color:
        :param position:
        :return: -1 - out of box
                  0 - empty
                  1 - own
                  2 - opponent
        """
        # Move to positions out of box are ot allowed
        if position.x > 7 or position.x < 0 or position.y > 7 or position.y < 0:
            return -1

        # Check for target of move
        figure = self.board[position.index]
        if figure is None:
            return 0

        # Can't move to same player's figure, otherwise we can
        return 2 if figure.color != color else 1
