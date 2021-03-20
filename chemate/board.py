from chemate.figure import King
from chemate.utils import Movement


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

    def get_figure(self, position):
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
                taken_figure=taken,
                is_rook=False
            )
        )
        self.board[from_pos.index] = None
        self.board[to_pos.index] = figure
        figure.position = to_pos

    def rollback_move(self):
        """
        Rollback last move
        :return: None
        """
        if len(self.moves) == 0:
            return

        last_move = self.moves.pop()
        self.board[last_move.from_pos.index] = last_move.figure
        self.board[last_move.to_pos.index] = last_move.taken_figure
        last_move.figure.position = last_move.from_pos
        if last_move.taken_figure is not None:
            self.balance += last_move.taken_figure.price

        if last_move.is_rook:
            self.rollback_move()

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
        :return: 0 - empty
                 1 - opponent figure
                 2 - own figure
                 3 - out of box
        """
        # Move to positions out of box are ot allowed
        if position.x > 7 or position.x < 0 or position.y > 7 or position.y < 0:
            return 3

        # Check for target of move
        figure = self.board[position.index]
        if figure is None:
            return 0

        # Can't move to same player's figure, otherwise we can
        return 1 if figure.color != color else 2

    def all_moves(self, color=None, taken_only=False):
        """
        Return list of available moves without
        :param color:
        :param taken_only:
        :return: Iterator object
        """
        for figure in self.board:
            if figure is not None and (color is None or figure.color == color):
                for pos in figure.available_moves():
                    taken = self.get_figure(pos)
                    if taken is not None or not taken_only:
                        yield Movement(figure, figure.position, pos, taken, False)
        pass

    def legal_moves(self, color):
        """
        Return only legal moves for player
        :param color: player color
        :return: list of Movement object
        """
        our_moves = list(self.all_moves(color))
        legal_moves = []
        for m in our_moves:
            # Try to make move and when check position
            self.make_move(m.from_pos, m.to_pos)
            if not self.has_check(color):
                legal_moves.append(m)
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
