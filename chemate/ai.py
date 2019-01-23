from chemate.player import Player
from chemate.utils import Position
import random


class DecisionTree(object):
    def __init__(self, board, max_level):
        self.board = board
        self.max_level = max_level
        self.best_moves = None
        self._central = [Position('d4'), Position('e4'), Position('d5'), Position('e5')]
        pass

    def next_move(self, color, level=0, alpha=-1000, beta=1000):
        """
        Main method for computer chess
        Make the best mevement for current
        :return:
        """
        best_moves = []
        min_max = None

        if level >= self.max_level:
            return self.estimate()

        # 1. Generate all available movements in current position
        for figure in filter(lambda x: x.color == color, self.board.figures()):
            for new_position in figure.available_moves():
                # 2. Make the ours movement
                figure.move(new_position)

                # 3. Make the best movement for opponent
                # return estimate and then rollback
                current_estimate = self.next_move(-color, level+1, alpha, beta)
                # 4. If current estimate is best then save this movement
                if min_max is None or \
                        (color == Player.WHITE and current_estimate >= min_max) or \
                        (color == Player.BLACK and current_estimate <= min_max):
                    if min_max != current_estimate:
                        best_moves = []
                    min_max = current_estimate
                    best_moves.append(self.board.moves[-1])

                # 4. Rollback ours movement
                self.board.rollback_move()

                # 5. Don't search for already bad movements
                if color == Player.WHITE:
                    if alpha is None or current_estimate > alpha:
                        alpha = current_estimate
                else:
                    if beta is None or current_estimate < beta:
                        beta = current_estimate

                if beta <= alpha:
                    return min_max
        if level == 0:
            self.best_moves = best_moves

        if min_max is None:
            # No available moves
            return 1000 * color
        return min_max

    def estimate(self):
        """
        Estimate current position for self.color figures
        :return:
        """
        # Estimate quality position
        quality_estimate = self.board.balance

        position_estimate = 0.0
        # Position estimate if quality is equal
        if quality_estimate == 0:
            for pos in self._central:
                fig = self.board.get_figure(pos)
                if fig is not None:
                    position_estimate += 0.05 * fig.color

        return quality_estimate + position_estimate
