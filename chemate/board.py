from chemate.figure import Pawn, Rook, Knight, Bishop, Queen, King
from chemate.player import Player
from chemate.utils import Position


class Board(object):
    def __init__(self):
        self.board = None
        self.clear()
        pass

    def print(self):
        """
        Print current state of the board for debug
        :return: None
        """
        for y in range(7, -1, -1):
            print(
                "".join(
                    ["_" if self.board[y*8 + x] is None else self.board[y*8 + x].char
                     for x in range(0, 8, 1)]
                )
            )
            pass
        pass

    def clear(self):
        """
        Clears the board
        :return: None
        """
        self.board = [None for x in range(64)]

    def copy(self):
        """
        Return full copy the current board
        :return: Board object
        """
        new_board = self.__class__()
        new_board.put_figures(map(lambda x: x.copy(), self.figures()))
        return new_board

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
        pass

    def move_figure(self, from_pos, to_pos):
        """
        Move figure to the new location
        :param from_pos:
        :param to_pos:
        :return: None
        """
        figure = self.board[from_pos.index]
        self.board[from_pos.index] = None
        self.board[to_pos.index] = figure

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

    def can_move(self, color, position, only_empty=False, only_opposite=False):
        """
        Check for player can make the move
        :param color:
        :param position:
        :param only_empty:
        :param only_opposite:
        :return: True if this move is allowed and False otherwise
        """
        # Move to positions out of box are ot allowed
        if position.x > 7 or position.x < 0 or position.y > 7 or position.y < 0:
            return False

        # Check for target of move
        figure = self.board[position.index]
        if figure is None:
            return not only_opposite

        # Can't move to same player's figure, otherwise we can
        return figure.color != color and not only_empty
