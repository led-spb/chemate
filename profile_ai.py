import cProfile
from chemate.board import Board
from chemate.ai import DecisionTree


def start():
    board = Board()
    board.initial_position()
    decision = DecisionTree(board, max_level=3)
    decision.best_move(1)


cProfile.run('start()', sort=2)

