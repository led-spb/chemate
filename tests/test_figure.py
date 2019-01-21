from chemate.figure import *
from chemate.player import Player
from chemate.board import Board
from chemate.utils import *
from pytest import fixture


@fixture(name="board")
def init_board():
    board = Board()
    yield board


class TestPawn(object):
    def test_first_move(self, board):
        # White pawn can move 2 on up at first
        p1 = Pawn(Player.WHITE, Position(3, 1))
        board.put_figure(p1)

        moves = list(p1.available_moves())
        assert len(moves) == 2
        assert Position(3, 2) in moves and Position(3, 3) in moves

        # After this only one
        p1.move(Position(3, 2))
        moves = list(p1.available_moves())
        assert len(moves) == 1
        assert Position(3, 3) in moves

        # Black pawn can move 2 on down
        p2 = Pawn(Player.BLACK, Position(1, 6))
        board.put_figure(p2)

        moves = list(p2.available_moves())
        assert Position(1, 5) in moves and Position(1, 4) in moves

        p2.move(Position(1, 4))
        moves = list(p2.available_moves())
        assert len(moves) == 1
        assert Position(1, 3) in moves

    def test_blocked(self, board):
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
