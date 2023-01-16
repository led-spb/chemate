import cProfile
from chemate.board import Board
from chemate.decision import DecisionTree
from chemate.positions import InitialPosition
from chemate.core import Player


def start():
    board = Board(InitialPosition())
    decision = DecisionTree(board, max_level=4)
    decision.best_move(Player.WHITE)


if __name__ == '__main__':
    cProfile.run('start()', filename='output.prof')
