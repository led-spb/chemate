import functools
import itertools
import multiprocessing
import random

from chemate.board import Board
from chemate.core import Position, Player, Movement


class DecisionTree(object):
    _central = [Position.from_char('d4'),
                Position.from_char('e4'),
                Position.from_char('d5'),
                Position.from_char('e5')]

    """ 
    This class realize decision tree algorithm
    """
    def __init__(self, max_level: int) -> None:
        self.board = None
        self.max_level = max_level
        pass

    def estimate_move(self, variants: int, color: int, depth: int, alpha: int, beta: int, move: Movement) -> tuple[float, int]:
        self.board.move(move)
        score, variants = self.mini_max(variants+1, -color, depth-1, alpha, beta)
        self.board.rollback()
        return score, variants

    def best_move(self, board: Board, depth: int = None) -> tuple[Movement, float, int]:
        self.board = board
        depth = depth or self.max_level
        color = self.board.current
        best_move = None
        best_score = -9999 if color == Player.WHITE else 9999

        total_variants = 0
        pool = multiprocessing.Pool()

        try:
            moves, all_moves = list(itertools.tee(self.board.valid_moves(color), 2))
            func = functools.partial(self.estimate_move, 1, color, depth, -10000, +10000)
            for score, variants in pool.imap(func, moves):
                move = next(all_moves)
                total_variants += variants
                if (color == Player.WHITE and score > best_score) or (color == Player.BLACK and score < best_score) \
                        or best_move is None:
                    best_move = move
                    best_score = score
        finally:
            pool.close()
        return best_move, best_score, total_variants

    def mini_max(self, variants: int, color: int, depth: int, alpha: float, beta: float) -> tuple[float, int]:
        """
        Main method for computer chess
        Make the best movement for current
        :return: Estimated position cost
        """
        # At leaf return estimate
        if depth <= 0:
            return self.estimate(), variants

        best_score = -9999 if color == Player.WHITE else 9999

        # Generate all available movements in current position
        for move in self.board.valid_moves(color):
            # Move own figure
            score, variants = self.estimate_move(variants+1, color, depth-1, alpha, beta, move)

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
                return best_score, variants
        return best_score, variants

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
