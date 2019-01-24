from chemate.figure import *
from chemate.utils import Position
from chemate.board import Board
from chemate.ai import DecisionTree
from chemate.image.draw import Draw
import random
import pytest
from wand.image import Image

class TestAI(object):

    @staticmethod
    def make_moves(board, decision, color, count):
        gif = Image()

        for i in range(count):
            drw = Draw()
            move, estimate = decision.best_move(color, draw=drw)

            move.figure.move(move.to_pos)
            print()
            print(
                "%d: %s %s (%.2f)" %
                (i + 1, 'white' if color == Player.WHITE else 'black', str(move), estimate)
            )
            print(str(board))
            color = -color
            drw.draw_board(board)

            img = drw.image
            gif.sequence.append(drw.image)
            gif.sequence[-1].delay = 300

        gif.type = 'optimize'
        gif.save(filename='moves.gif')

    # @pytest.mark.skip
    def test_select_move(self):
        board = Board()

        board.initial_position()
        decision = DecisionTree(board=board, max_level=5)
        assert abs(decision.estimate()) <= 0.5
        self.make_moves(board, decision, Player.WHITE, 10)

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
        decision = DecisionTree(board=board, max_level=2*2)

        print("0: (%.2f)" % decision.estimate())
        print(str(board))
        self.make_moves(board, decision, Player.WHITE, 6)

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

    def test_case_3(self):
        board = Board()
        q = [
            Queen(Player.WHITE, Position('b6')),

           # Pawn(Player.BLACK, Position('h6')),
            Rook(Player.BLACK, Position('a6')),
        ]
        board.put_figures(q)
        decision = DecisionTree(board=board, max_level=2*2)

        print("0: (%.2f)" % decision.estimate())
        print(str(board))
        self.make_moves(board, decision, Player.WHITE, 1)

    def test_case_3(self):
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
