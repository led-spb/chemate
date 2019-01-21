from chemate.board import Board
from chemate.figure import *
from chemate.player import Player


class TestGame(object):

    def test_game_init(self):
        board = Board()
        board.initial_position()

        assert len(list(board.figures())) == 32

        assert len(list(filter(lambda x: x.color == Player.WHITE, board.figures()))) == 16
        assert len(list(filter(lambda x: x.color == Player.BLACK, board.figures()))) == 16

        assert len(list(filter(lambda x: isinstance(x, Pawn), board.figures()))) == 16
        assert len(list(filter(lambda x: isinstance(x, Tower), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Horse), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Elephant), board.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Queen), board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, King), board.figures()))) == 2

        assert len(list(filter(lambda x: isinstance(x, Pawn) and x.color == Player.WHITE, board.figures()))) == 8
        assert len(list(filter(lambda x: isinstance(x, Pawn) and x.color == Player.BLACK, board.figures()))) == 8
        assert len(list(filter(lambda x: isinstance(x, Tower) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Tower) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Horse) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Horse) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Elephant) and x.color == Player.WHITE, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Elephant) and x.color == Player.BLACK, board.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, Queen) and x.color == Player.WHITE, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, Queen) and x.color == Player.BLACK, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, King) and x.color == Player.WHITE, board.figures()))) == 1
        assert len(list(filter(lambda x: isinstance(x, King) and x.color == Player.BLACK, board.figures()))) == 1
        pass
