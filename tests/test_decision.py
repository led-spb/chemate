from chemate.figures import *
from chemate.positions import InitialPosition, EmptyPosition
from chemate.core import Position, Player
from chemate.board import Board
from chemate.decision import DecisionTree
import pytest


@pytest.mark.skip
class TestDecision(object):

    @staticmethod
    def make_moves(board, decision, color, count):
        for i in range(count):
            move, estimate = decision.best_move(color)

            move.figure.move(move.to_pos)
            print(
                "%d: %s %s (%.2f)" %
                (i + 1, 'white' if color == Player.WHITE else 'black', str(move), estimate)
            )
            color = -color

    def test_game(self):
        board = Board(InitialPosition())

        board.init()
        decision = DecisionTree(board=board, max_level=2)
        assert abs(decision.estimate()) <= 0.5
        self.make_moves(board, decision, Player.WHITE, 30)

    def test_case_1(self):
        board = Board(EmptyPosition())
        q = [
            Queen(Player.WHITE, Position.from_char('d2')),

            Pawn(Player.BLACK, Position.from_char('h6')),
            Knight(Player.BLACK, Position.from_char('d4')),
            Rook(Player.BLACK, Position.from_char('a5')),
            Bishop(Player.BLACK, Position.from_char('d8'))
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=2)

        print("0: (%.2f)" % decision.estimate())
        self.make_moves(board, decision, Player.WHITE, 8)

    def test_case_2(self):
        board = Board(EmptyPosition())
        q = [
            Queen(Player.WHITE, Position.from_char('d4')),
            Bishop(Player.BLACK, Position.from_char('b6'))
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=2)

        print("0: (%.2f)" % decision.estimate())
        self.make_moves(board, decision, Player.WHITE, 1)

    def test_case_3(self):
        board = Board(EmptyPosition())
        q = [
            Queen(Player.WHITE, Position.from_char('b6')),
            Rook(Player.BLACK, Position.from_char('a6')),
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=2)

        print("0: (%.2f)" % decision.estimate())
        self.make_moves(board, decision, Player.WHITE, 1)

    def test_case_4(self):
        board = Board(EmptyPosition())
        q = [
            Bishop(Player.WHITE, Position.from_char('e8')),
            King(Player.BLACK, Position.from_char('d8')),
            King(Player.WHITE, Position.from_char('a1')),
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=2)

        print("0: (%.2f)" % decision.estimate())
        self.make_moves(board, decision, Player.BLACK, 1)
