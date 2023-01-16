from chemate.board import Board
from chemate.core import Position, Player, Movement
import random


class DecisionTree(object):
    _central = [Position.from_char('d4'),
                Position.from_char('e4'),
                Position.from_char('d5'),
                Position.from_char('e5')]

    """
    This class realize decision tree algorithm
    """
    def __init__(self, board: Board, max_level: int) -> None:
        self.board = board
        self.max_level = max_level
        # self._estimates = {}
        pass

    def best_move(self, color: int, depth: int = None) -> tuple[Movement, float]:
        """
        Select best move for player
        :param color: color of figures
        :param depth: number of moves for look
        :return: Movement object
        """
        depth = depth or self.max_level
        best_move = None
        best_score = -9999 if color == Player.WHITE else 9999

        for move in list(self.board.valid_moves(color)):
            self.board.move(move)
            try:
                score = self.mini_max(-color, depth-1, -10000, 10000)

                if (color == Player.WHITE and score > best_score) \
                        or (color == Player.BLACK and score < best_score):
                    best_move = move
                    best_score = score
            finally:
                self.board.rollback()

        return best_move, best_score

    def mini_max(self, color, depth, alpha, beta) -> float:
        """
        Main method for computer chess
        Make the best movement for current
        :return: Estimated position cost
        """
        # At leaf return estimate
        if depth == 0:
            return self.estimate()

        best_score = -9999 if color == Player.WHITE else 9999

        # Generate all available movements in current position
        for move in self.board.valid_moves(color):
            # Move own figure
            self.board.move(move)
            # Make opponent's move and check the position estimate
            score = self.mini_max(-color, depth-1, alpha, beta)
            # Rollback own movement
            self.board.rollback()

            if color == Player.WHITE:
                # We need select a move with max estimate
                if score > best_score:
                    best_score = score
                if best_score > alpha:
                    alpha = best_score
            else:
                # else select a move with min estimate
                if score < best_score:
                    best_score = score
                if best_score < beta:
                    beta = best_score

            if beta <= alpha:
                return best_score
        return best_score

    def estimate(self) -> float:
        """
        Estimate current position for self.color figures
        :return: float
        """
        # Estimate quality position
        quality_estimate = self.board.balance
        position_estimate = 0
        # Position estimate if quality is equal

        if quality_estimate == 0:
            for pos in self._central:
                fig = self.board.figure_at(pos)
                if fig is not None:
                    position_estimate += fig.price*0.5

        # Rook movement is preferred
        for move in self.board.moves:
            if move.rook is not None:
                position_estimate += 2*move.rook.color

        estimate = quality_estimate + position_estimate + (random.random()-0.5)
        return estimate
