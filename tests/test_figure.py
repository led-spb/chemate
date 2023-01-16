from chemate.figures import *
from chemate.board import Board
from chemate.positions import EmptyPosition


class TestFigure(object):
    def test_copy(self):
        """
        Testing copy figure, after copy new and old must be different objects
        :return:
        """
        board1 = Board()
        board1.init(EmptyPosition())
        board2 = Board()
        board2.init(EmptyPosition())
        p1 = Pawn(Player.WHITE, Position.from_char('e3'))
        board1.put_figure(p1)

        p2 = p1.copy()
        board2.put_figure(p2)
        assert p1 == p2

        board1.move(next(board1.figure_moves(p1)))
        assert p1 != p2


class TestBishop(object):
    def test_move(self):
        pass


class TestQueen(object):
    def test_move(self):
        pass
