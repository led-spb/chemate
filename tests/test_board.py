from chemate.board import Board
from chemate.figure import *
from chemate.player import Player


class TestBoard(object):

    def test_board_init(self):
        board = Board()
        board.initial_position()
        print()
        board.print()

        assert len(list(board.figures())) == 32

        assert len(list(filter(lambda x: x.color == Player.WHITE, board.figures()))) == 16
        assert len(list(filter(lambda x: x.color == Player.BLACK, board.figures()))) == 16

        assert len(list(filter(lambda x: isinstance(x, Pawn), board.figures()))) == 16
        assert len(list(filter(lambda x: isinstance(x, Rook), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Knight), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Bishop), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Queen), board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, King), board.figures()))) == 2

        assert len(list(filter(lambda x: isinstance(x, Pawn) and x.color == Player.WHITE, board.figures()))) == 8
        assert len(list(filter(lambda x: isinstance(x, Pawn) and x.color == Player.BLACK, board.figures()))) == 8
        assert len(list(filter(lambda x: isinstance(x, Rook) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Rook) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Knight) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Knight) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Bishop) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Bishop) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Queen) and x.color == Player.WHITE, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, Queen) and x.color == Player.BLACK, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, King) and x.color == Player.WHITE, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, King) and x.color == Player.BLACK, board.figures()))) == 1
        pass

    def test_board_move(self):
        board = Board()
        board.initial_position()
        board.make_move(Position.char('e2'), Position.char('e4'))
        board.print()
        assert len(board.moves) == 1
        board.rollback_move()
        board.print()
        assert len(board.moves) == 0
