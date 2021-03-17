from chemate.figure import *
from chemate.utils import Position
from chemate.board import Board
from chemate.decision import DecisionTree
#from chemate.image.draw import Draw
import pytest


class TestDecision(object):

    @staticmethod
    def make_moves(board, decision, color, count):
        for i in range(count):
            drw = Draw()
            move, estimate = decision.best_move(color, debug=None)

            move.figure.move(move.to_pos)
            print()
            print(
                "%d: %s %s (%.2f)" %
                (i + 1, 'white' if color == Player.WHITE else 'black', str(move), estimate)
            )
            print(str(board))
            color = -color
            drw.draw_board(board)
            drw.image.save(filename='move_%02d.png' % i)

    @pytest.mark.skip
    def test_game(self):
        board = Board()

        board.init()
        decision = DecisionTree(board=board, max_level=3)
        assert abs(decision.estimate()) <= 0.5
        self.make_moves(board, decision, Player.WHITE, 30)

    @pytest.mark.skip
    def test_case_1(self):
        board = Board()
        q = [
            Queen(Player.WHITE, Position('d2')),

            Pawn(Player.BLACK, Position('h6')),
            Knight(Player.BLACK, Position('d4')),
            Rook(Player.BLACK, Position('a5')),
            Bishop(Player.BLACK, Position('d8'))
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=3)

        print("0: (%.2f)" % decision.estimate())
        print(str(board))
        self.make_moves(board, decision, Player.WHITE, 8)

    @pytest.mark.skip
    def test_case_2(self):
        board = Board()
        q = [
            Queen(Player.WHITE, Position('d4')),
            Bishop(Player.BLACK, Position('b6'))
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=2*2)

        print("0: (%.2f)" % decision.estimate())
        print(str(board))

        self.make_moves(board, decision, Player.WHITE, 1)

    @pytest.mark.skip
    def test_case_3(self):
        board = Board()
        q = [
            Queen(Player.WHITE, Position('b6')),
            Rook(Player.BLACK, Position('a6')),
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=2*2)

        print("0: (%.2f)" % decision.estimate())
        print(str(board))
        self.make_moves(board, decision, Player.WHITE, 1)

    @pytest.mark.skip
    def test_case_4(self):
        board = Board()
        q = [
            Bishop(Player.WHITE, Position('e8')),
            King(Player.BLACK, Position('d8')),
            King(Player.WHITE, Position('a1')),

        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=3*2)

        print("0: (%.2f)" % decision.estimate())
        print(str(board))
        self.make_moves(board, decision, Player.BLACK, 1)
