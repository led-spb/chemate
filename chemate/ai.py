from chemate.player import Player
import random


class DecisionTree(object):
    def __init__(self, board, max_level):
        self.board = board
        self.max_level = max_level
        self.best_move = None
        pass

    def next_move(self, color, level=0, alpha=-256, beta=256):
        """
        Main method for computer chess
        Make the best mevement for current
        :return:
        """
        best_move = None
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
                current_estimate = self.next_move(not color, level+1, alpha, beta)

                # 4. If current estimate is best then save this movement
                if min_max is None or \
                        (color == Player.WHITE and current_estimate > min_max) or \
                        (color == Player.BLACK and current_estimate <= min_max):
                    min_max = current_estimate
                    best_move = self.board.moves[-1]

                # 4. Rollback ours movement
                self.board.rollback_move()

                # 5. Don't search for already bad movements
                if color == Player.WHITE:
                    if alpha is None or current_estimate > alpha:
                        alpha = current_estimate
                else:
                    if beta is None or current_estimate < beta:
                        beta = current_estimate

                if beta < alpha:
                    return min_max if min_max is not None else self.estimate()

        # At final store the best move
        if level == 0:
            self.best_move = best_move
        return min_max if min_max is not None else self.estimate()

    def estimate(self):
        """
        Estimate current position for self.color figures
        :return:
        """
        return random.randint(0, 255)
