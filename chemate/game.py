import json
from chemate.figure import Pawn, Tower, Horse, Elephant, Queen, King
from chemate.player import Player
from chemate.utils import Position


class Game(object):
    def __init__(self, players):
        self.board = None
        self.init_board()
        self.players = players
        pass

    def init_board(self):
        self.board = [None for x in range(64)]
        # Pawns
        for i in range(8):
            self.put_figure(Pawn(Player.WHITE, self, Position(i, 1)))
            self.put_figure(Pawn(Player.BLACK, self, Position(i, 6)))
        # Towers
        for i in range(0, 8, 7):
            self.put_figure(Tower(Player.WHITE, self, Position(i, 0)))
            self.put_figure(Tower(Player.BLACK, self, Position(i, 7)))
        # Horses
        for i in range(1, 7, 5):
            self.put_figure(Horse(Player.WHITE, self, Position(i, 0)))
            self.put_figure(Horse(Player.BLACK, self, Position(i, 7)))
        # Elephants
        for i in range(2, 6, 3):
            self.put_figure(Elephant(Player.WHITE, self, Position(i, 0)))
            self.put_figure(Elephant(Player.BLACK, self, Position(i, 7)))
        # Queens
        self.put_figure(Queen(Player.WHITE, self, Position(3, 0)))
        self.put_figure(Queen(Player.BLACK, self, Position(3, 7)))
        # Kings
        self.put_figure(King(Player.WHITE, self, Position(4, 0)))
        self.put_figure(King(Player.BLACK, self, Position(4, 7)))

    @property
    def state(self):
        """
        Return current state of game
        :return: Dictionary object with next structure:
        players: tuple with two items: (white player name, black player name)
        moves: list of moves
        board:
        status:
s        message:
        """
        return {}

    def put_figure(self, figure):
        """
        Put a figure on the board
        :return: None
        """
        self.board[figure.position.y*8 + figure.position.x] = figure
        pass

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
        # Move to positions out of box not allowed
        if position.x > 7 or position.x < 0 or position.y > 7 or position.y < 0:
            return False

        # Check fot target of move
        figure = self.board[position.y*8 + position.y]
        if figure is None:
            return not only_empty and not only_opposite

        # Can't move to same player's figure, otherwise we can
        return figure.color != color
