from chemate.player import Player
from chemate.board import Board
from chemate.ai import DecisionTree


class TestAI(object):
    def test_select_move(self):
        board = Board()
        board.initial_position()

        decision = DecisionTree(Player.WHITE, board, 0, 1)
        move = decision.next_move()

        print("Estimate: %.2f" % move.estimate)
        move.decision.board.print()
