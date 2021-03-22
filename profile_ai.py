import cProfile
from chemate.board import Board
from chemate.decision import DecisionTree
from chemate.positions import InitialPosition


def start():
    board = Board(InitialPosition())
    decision = DecisionTree(board, max_level=2)
    decision.best_move(1)


cProfile.run('start()', sort="time")
