from chemate.utils import Position, Player
import random


class DecisionTree(object):
    """
    This class realize decision tree algorithm
    """
    def __init__(self, board, max_level):
        self.board = board
        self.best_moves = None
        self.max_level = max_level
        self._central = [Position('d4'), Position('e4'), Position('d5'), Position('e5')]
        self._estimates = {}
        pass

    def best_move(self, color, depth=None):
        """
        Select best move for player
        :param color: color of figures
        :param depth: number of moves for look
        :return: Movement object
        """
        depth = depth or self.max_level
        best_move = None
        best_score = -9999 if color == Player.WHITE else 9999

        for move in self.board.legal_moves(color):
            self.board.make_move(move.from_pos, move.to_pos)
            score = self.mini_max(-color, depth-1, -10000, 10000)

            if (color == Player.WHITE and score > best_score) \
                    or (color == Player.BLACK and score < best_score):
                best_move = move
                best_score = score
            self.board.rollback_move()

        return best_move, best_score

    def mini_max(self, color, depth, alpha, beta):
        """
        Main method for computer chess
        Make the best mevement for current
        :return: Estimated position cost
        """
        # At leaf return estimate
        if depth == 0:
            return self.estimate()

        best_score = -9999 if color == Player.WHITE else 9999

        # Generate all available movements in current position
        for move in self.board.legal_moves(color):
            # Move own figure
            self.board.make_move(move.from_pos, move.to_pos)
            # Make opponent's move and check the position estimate
            score = self.mini_max(-color, depth-1, alpha, beta)
            # Rollback own movement
            self.board.rollback_move()

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

    def estimate(self):
        """
        Estimate current position for self.color figures
        :return:
        """
        h = hash(self.board)
        if h in self._estimates:
            return self._estimates[h]

        # Estimate quality position
        quality_estimate = self.board.balance

        position_estimate = 0
        # Position estimate if quality is equal

        if quality_estimate == 0:
            for pos in self._central:
                fig = self.board.get_figure(pos)
                if fig is not None:
                    position_estimate += fig.price*0.5

        estimate = quality_estimate + position_estimate + (random.random()-0.5)
        self._estimates[h] = estimate
        return estimate
