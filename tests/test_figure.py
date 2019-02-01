from chemate.figure import *
from chemate.board import Board
from chemate.utils import *


class TestFigure(object):
    def test_copy(self):
        """
        Testing copy figure, after copy new and old must be different objects
        :return:
        """
        board1 = Board()
        board2 = Board()
        p1 = Pawn(Player.WHITE, Position(3, 3))
        board1.put_figure(p1)

        p2 = p1.copy()
        board2.put_figure(p2)
        assert p1 == p2

        p1.move(Position(3, 4))
        assert p1 != p2


class TestPawn(object):
    def test_first_move(self):
        board = Board()

        # 1. White pawn can move 2 on up at first
        p1 = Pawn(Player.WHITE, Position('d2'))
        board.put_figure(p1)
        moves = list(p1.available_moves())
        assert len(moves) == 2
        assert Position('d3') in moves and Position('d4') in moves

        # 2. After this only one
        p1.move(Position('d3'))
        moves = list(p1.available_moves())
        assert len(moves) == 1
        assert Position('d4') in moves

        # 3. Black pawn can move 2 on down
        p2 = Pawn(Player.BLACK, Position('b7'))
        board.put_figure(p2)
        moves = list(p2.available_moves())
        assert Position('b6') in moves and Position('b5') in moves

        p2.move(Position('b5'))
        moves = list(p2.available_moves())
        assert len(moves) == 1
        assert Position('b4') in moves

    def test_blocked(self):
        board = Board()

        # Blocked by end of board
        p1 = Pawn(Player.WHITE, Position(1, 7))
        board.put_figure(p1)
        moves = list(p1.available_moves())
        assert len(moves) == 0

        # Blocked by own figure
        p2 = Pawn(Player.WHITE, Position(1, 6))
        board.put_figure(p2)
        moves = list(p2.available_moves())
        assert len(moves) == 0

        # Blocked by opposite figure and fight
        p1 = Pawn(Player.WHITE, Position(3, 3))
        p2 = Pawn(Player.WHITE, Position(4, 3))

        p3 = Pawn(Player.BLACK, Position(3, 4))
        p4 = Pawn(Player.BLACK, Position(4, 4))
        board.put_figure(p1)
        board.put_figure(p2)
        board.put_figure(p3)
        board.put_figure(p4)

        print()
        print(board)

        moves = list(p1.available_moves())
        assert len(moves) == 1
        assert Position(4, 4) in moves

        moves = list(p2.available_moves())
        assert len(moves) == 1
        assert Position(3, 4) in moves

        moves = list(p3.available_moves())
        assert len(moves) == 1
        assert Position(4, 3) in moves

        moves = list(p4.available_moves())
        assert len(moves) == 1
        assert Position(3, 3) in moves
        pass


class TestKnight(object):
    def test_move(self):
        board = Board()
        knight = Knight(Player.BLACK, Position.char('D5'))
        board.put_figure(knight)
        for pos in knight.available_moves():
            knight.move(pos)
            assert len(board.moves) == 1
            board.rollback_move()
            assert len(board.moves) == 0


class TestKing(object):
    def test_move(self):
        board = Board()
        king = King(Player.WHITE, Position('c3'))
        board.put_figure(king)
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 8

        king.move(Position('a1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 3


class TestBishop(object):
    def test_move(self):
        pass


class TestQueen(object):
    def test_move(self):
        pass


class TestRook(object):
    def test_fight_blocked(self):
        board = Board()
        rook = Rook(Player.WHITE, Position.char('A3'))
        pawn = Pawn(Player.BLACK, Position.char('B3'))
        p2 = Knight(Player.WHITE, Position.char('A5'))
        bishop = Bishop(Player.BLACK, Position.char('H3'))

        board.put_figures([rook, pawn, p2, bishop])

        for pos in rook.available_moves():
            assert pos != Position.char('C3')
            assert pos != Position.char('A5')
            board.rollback_move()
