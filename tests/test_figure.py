import pytest
from chemate.figure import *
from chemate.board import Board
from chemate.positions import EmptyPosition, PredefinedFENPosition
from chemate.utils import *


class TestFigure(object):
    def test_copy(self):
        """
        Testing copy figure, after copy new and old must be different objects
        :return:
        """
        board1 = Board(EmptyPosition())
        board2 = Board(EmptyPosition())
        p1 = Pawn(Player.WHITE, Position.from_char('e3'))
        board1.put_figure(p1)

        p2 = p1.copy()
        board2.put_figure(p2)
        assert p1 == p2

        p1.move(Position.from_char('e4'))
        assert p1 != p2


class TestPawn(object):
    def test_first_move(self):
        board = Board(EmptyPosition())

        # 1. White pawn can move 2 on up at first
        p1 = Pawn(Player.WHITE, Position.from_char('d2'))
        board.put_figure(p1)
        moves = list(map(str, p1.available_moves(hash(board))))
        assert len(moves) == 2
        assert 'd2-d3' in moves and 'd2-d4' in moves

        # 2. After this only one
        p1.move(Position.from_char('d3'))
        moves = list(map(str,p1.available_moves(hash(board))))
        assert len(moves) == 1
        assert 'd3-d4' in moves

        # 3. Black pawn can move 2 on down
        p2 = Pawn(Player.BLACK, Position.from_char('b7'))
        board.put_figure(p2)
        moves = list(map(str, p2.available_moves(hash(board))))
        assert 'b7-b6' in moves and 'b7-b5' in moves

        p2.move(Position.from_char('b5'))
        moves = list(map(str, p2.available_moves(hash(board))))
        assert len(moves) == 1
        assert 'b5-b4' in moves

    def test_blocked(self):
        board = Board(EmptyPosition())

        # Blocked by end of board
        a8 = Pawn(Player.WHITE, Position.from_char('a8'))
        board.put_figure(a8)
        moves = list(a8.available_moves(hash(board)))
        assert len(moves) == 0

        # Blocked by own figure
        e4 = Pawn(Player.WHITE, Position.from_char('a7'))
        board.put_figure(e4)
        moves = list(e4.available_moves(hash(board)))
        assert len(moves) == 0

        # Blocked by opposite figure and fight
        d4 = Pawn(Player.WHITE, Position.from_char('d4'))
        e4 = Pawn(Player.WHITE, Position.from_char('e4'))
        d5 = Pawn(Player.BLACK, Position.from_char('d5'))
        e5 = Pawn(Player.BLACK, Position.from_char('e5'))
        board.put_figures([d4, e4, d5, e5])

        moves = list(map(str, d4.available_moves(hash(board))))
        assert len(moves) == 1
        assert 'd4-e5' in moves

        moves = list(map(str, e4.available_moves(hash(board))))
        assert len(moves) == 1
        assert 'e4-d5' in moves

        moves = list(map(str, d5.available_moves(hash(board))))
        assert len(moves) == 1
        assert 'd5-e4' in moves

        moves = list(map(str, e5.available_moves(hash(board))))
        assert len(moves) == 1
        assert 'e5-d4' in moves
        pass

    def test_transform(self):
        board = Board(PredefinedFENPosition('7n/P5P1/8/8/8/8/p5p1/7N'))

        # White
        a7 = board.get_figure(Position.from_char('a7'))
        moves = list(a7.available_moves(hash(board)))
        assert len(moves) == 4, "White pawn can transform to 4 figures"

        move = next(filter(lambda x: isinstance(x.transform_to, Queen), moves))
        board.make_move(move)

        a8 = board.get_figure(Position.from_char('a8'))
        assert isinstance(a8, Queen) and a8.color == Player.WHITE
        assert board.get_figure(Position.from_char('a7')) is None

        g7 = board.get_figure(Position.from_char('g7'))
        moves = list(g7.available_moves(hash(board)))
        assert len(moves) == 8
        move = next(filter(lambda x: isinstance(x.transform_to, Queen) and x.to_pos == Position.from_char('h8'), moves))
        board.make_move(move)
        h8 = board.get_figure(Position.from_char('h8'))
        assert isinstance(h8, Queen) and h8.color == Player.WHITE
        assert board.get_figure(Position.from_char('g7')) is None

        # Black
        a2 = board.get_figure(Position.from_char('a2'))
        moves = list(a2.available_moves(hash(board)))
        assert len(moves) == 4, "White pawn can transform to 4 figures"

        move = next(filter(lambda x: isinstance(x.transform_to, Queen), moves))
        board.make_move(move)

        a1 = board.get_figure(Position.from_char('a1'))
        assert isinstance(a1, Queen) and a1.color == Player.BLACK
        assert board.get_figure(Position.from_char('a2')) is None

        g2 = board.get_figure(Position.from_char('g2'))
        moves = list(g2.available_moves(hash(board)))
        assert len(moves) == 8
        move = next(filter(lambda x: isinstance(x.transform_to, Queen) and x.to_pos == Position.from_char('h1'), moves))
        board.make_move(move)
        h1 = board.get_figure(Position.from_char('h1'))
        assert isinstance(h1, Queen) and h1.color == Player.BLACK
        assert board.get_figure(Position.from_char('g2')) is None


class TestKnight(object):
    def test_move(self):
        board = Board(EmptyPosition())
        knight = Knight(Player.BLACK, Position.from_char('d5'))
        board.put_figure(knight)
        for move in knight.available_moves(hash(board)):
            knight.move(move.to_pos)
            assert len(board.moves) == 1
            board.rollback_move()
            assert len(board.moves) == 0


class TestKing(object):
    def test_move(self):
        board = Board(EmptyPosition())
        king = King(Player.WHITE, Position.from_char('c3'))
        board.put_figure(king)
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 8

        king.move(Position.from_char('a1'))
        moves = board.legal_moves(Player.WHITE)
        assert len(moves) == 3

    def test_rook(self):
        board = Board(EmptyPosition())
        king = King(Player.WHITE, Position.from_char('e1'))
        rook = Rook(Player.WHITE, Position.from_char('h1'))
        board.put_figures([king, rook])


class TestBishop(object):
    def test_move(self):
        pass


class TestQueen(object):
    def test_move(self):
        pass


class TestRook(object):
    def test_fight_blocked(self):
        board = Board(EmptyPosition())
        rook = Rook(Player.WHITE, Position.from_char('a3'))
        pawn = Pawn(Player.BLACK, Position.from_char('b3'))
        p2 = Knight(Player.WHITE, Position.from_char('a5'))
        bishop = Bishop(Player.BLACK, Position.from_char('h3'))

        board.put_figures([rook, pawn, p2, bishop])

        for movement in rook.available_moves(hash(board)):
            assert movement.to_pos != Position.from_char('a3')
            assert movement.to_pos != Position.from_char('a5')
        pass

    @pytest.mark.skip
    def test_rook(self):
        pass
