from typing import Iterator

from chemate.figure import King, Figure
from chemate.utils import Movement, Position


class Board(object):
    def __init__(self, position_factory):
        self.position_factory = position_factory
        self.board = None
        self.moves = []
        self.balance = 0
        self.init()

    def __hash__(self):
        """
        Calculates hash for current position
        :return:
        """
        lst = ['.' if x is None else x.char for x in self.board]
        s = ''.join(lst)
        return s.__hash__()

    def clear(self):
        """
        Clears the board
        :return: None
        """
        self.board = [None for x in range(64)]

    def init(self):
        """
        Generate initial state of board
        :return: None
        """
        self.clear()
        self.put_figures(self.position_factory.figures())

    def put_figure(self, figure):
        """
        Put a figure on the board
        :return: None
        """
        self.board[figure.position.y * 8 + figure.position.x] = figure
        figure.board = self
        self.balance += figure.price
        pass

    def get_figure(self, position) -> Figure:
        """
        Get figure at specified location on board
        :param position: Position on board
        :return: Figure instance or None
        """
        return self.board[position.index]

    def find_figures(self, figure_class, color=None):
        for figure in self.figures():
            if isinstance(figure, figure_class) and (color is None or figure.color == color):
                yield figure
        pass

    def make_move(self, move):
        """
        Move figure to the new location
        :type move: Movement
        :return: None
        """
        if move.figure is None:
            move.figure = self.board[move.from_pos.index]
        if move.taken_figure is None:
            move.taken_figure = self.board[move.to_pos.index]
        if move.taken_figure is not None:
            self.balance -= move.taken_figure.price
        if move.transform_to is not None:
            self.balance += move.transform_to.price

        self.moves.append(move)
        figure = move.transform_to or move.figure
        self.board[move.from_pos.index] = None
        self.board[move.to_pos.index] = figure
        figure.position = move.to_pos
        figure.board = self

        # make rook movement
        if move.rook is not None:
            rook = move.rook
            long = rook.position.x - move.from_pos.x < 0
            new_rook_pos = Position.from_xy(3 if long else 5, rook.position.y)
            self.board[rook.position.index] = None
            self.board[new_rook_pos.index] = rook
            rook.position = new_rook_pos
        pass

    def rollback_move(self):
        """
        Rollback last move
        :return: BaseMovement
        """
        if len(self.moves) == 0:
            return

        last_move = self.moves.pop()
        self.board[last_move.from_pos.index] = last_move.figure
        self.board[last_move.to_pos.index] = last_move.taken_figure or None
        last_move.figure.position = last_move.from_pos

        # Restore rook position
        if last_move.rook is not None:
            rook = last_move.rook
            long = rook.position.x - last_move.from_pos.x < 0
            new_rook_pos = Position.from_xy(0 if long else 7, rook.position.y)
            self.board[rook.position.index] = None
            self.board[new_rook_pos.index] = rook
            rook.position = new_rook_pos

        # Restore balance
        if last_move.taken_figure is not None:
            self.balance += last_move.taken_figure.price
        if last_move.transform_to is not None:
            self.balance -= last_move.transform_to.price
        return last_move

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

    def all_moves(self, color=None, taken_only=False) -> Iterator[Movement]:
        """
        Return list of available moves without
        :param color: only for figures of specified color
        :param taken_only: only move when have take another figure
        :return: Iterator object
        """
        for figure in self.board:
            if figure is None or (color is not None and figure.color != color):
                continue
            for move in figure.available_moves():
                taken = self.get_figure(move.to_pos)
                if taken is not None or not taken_only:
                    move.taken_figure = taken
                    yield move
        pass

    def legal_moves(self, color, figure=None):
        """
        Return only legal moves for player
        :param figure: Figure
        :param color: player color
        :return: list of Movement object
        """
        legal_moves = []
        for move in self.all_moves(color):
            if figure is not None and move.figure != figure:
                continue
            # Try to make move and when check position
            self.make_move(move)
            if not self.has_check(color):
                legal_moves.append(move)
            self.rollback_move()
        return legal_moves

    def has_check(self, color):
        """
        Return true if current position has check for color player
        :param color:
        :return:
        """
        for opposite_move in self.all_moves(color=-color, taken_only=True):
            if isinstance(opposite_move.taken_figure, King):
                return True
        return False

    def has_mate(self, color):
        """
        Return true if current position has checkmate for color player
        :param color:
        :return:
        """
        return self.has_check(color) and list(self.legal_moves(color)) == []

    def has_moved(self, figure):
        """
        Check for figure has moved
        :param figure:
        :return:
        """
        for m in self.moves:
            if m.figure == figure:
                return True
        return False
