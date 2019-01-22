from chemate.player import Player
from collections import namedtuple
import random


class Movement(object):
    def __init__(self, decision, from_pos, to_pos, estimate=None):
        self.decision = decision
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.estimate = estimate


class DecisionTree(object):
    def __init__(self, color, board, level, max_level):
        self.color = color
        self.level = level
        self.board = board
        self.max_level = max_level
        self.variants = []
        pass

    def next_move(self):
        """
        Main method for computer chess
        Select best move for color
        :return: Tuple (from, to)
        """

        if self.level > self.max_level:
            return None

        # 1. Generate all available movements in current position
        for figure in filter(lambda x: x.color == self.color, self.board.figures()):
            for new_position in figure.available_moves():
                # 2. Make the ours movement
                new_board = self.board.copy()
                new_board.get_figure( figure.position ).move(new_position)

                # 3. Select and make the best movement for opponent
                opponent_decision = DecisionTree(
                    Player.WHITE if self.color == Player.BLACK else Player.BLACK,
                    new_board,
                    self.level+1, self.max_level
                )
                opponent_move = opponent_decision.next_move()
                if opponent_move is not None:
                    # 3.1 Movement opponent`s figure
                    new_board.get_figure(opponent_move.from_pos).move(opponent_move.to_pos)

                # 4. Save ours movement for further estimate
                self.variants.append(
                    Movement(
                        decision=DecisionTree(self.color, new_board, self.level+1, self.max_level),
                        from_pos=figure.position,
                        to_pos=new_position,
                        estimate=None
                    )
                )
                pass

        # 5. Select the ours movement with best estimate
        best_move = self.variants[0]
        for variant in self.variants:
            variant.estimate = variant.decision.estimate()
            if variant.estimate > best_move.estimate or best_move.estimate is None:
                best_move = variant
        # print("Color: %s, estimate: %.2f" % ('WHITE' if self.color == Player.WHITE else 'BLACK', best_move.estimate))
        # best_move.decision.board.print()
        return best_move

    def estimate(self):
        """
        Estimate current position for self.color figures
        :return:
        """
        # If current search depth < max level, search next best movement
        if self.level<self.max_level:
            next_move = self.next_move()
            return next_move.estimate
        else:
            return random.randint(0, 255)
