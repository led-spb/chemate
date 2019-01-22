import cProfile
from chemate.board import Board
from chemate.ai import DecisionTree


def start():
    board = Board()
    board.initial_position()
    decision = DecisionTree(board, 4)
    decision.next_move(True, 0)


cProfile.run('start()', sort=0)

