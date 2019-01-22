from chemate.player import Player
from chemate.board import Board
from chemate.ai import DecisionTree
import pytest


class TestAI(object):
    #@pytest.mark.skip
    def test_select_move(self):
        board = Board()
        board.initial_position()

        decision = DecisionTree(board=board, max_level=2*2)
        color = Player.WHITE
        for i in range(4):
            estimate = decision.next_move(color)

            print()
            print("%d: %s (%.2f)" % (i+1, str(decision.best_move), estimate))
            decision.best_move.figure.move(decision.best_move.to_pos)
            print(str(board))

            color = not color
