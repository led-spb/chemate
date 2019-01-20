import pytest
from chemate.game import Game
from chemate.figure import *
from chemate.player import Player


class TestGame(object):

    def test_game_init(self):
        game = Game([])
        assert len(list(game.figures())) == 32

        assert len(list(filter(lambda x: x.color == Player.WHITE, game.figures()))) == 16
        assert len(list(filter(lambda x: x.color == Player.BLACK, game.figures()))) == 16

        assert len(list(filter(lambda x: isinstance(x, Pawn), game.figures()))) == 16
        assert len(list(filter(lambda x: isinstance(x, Tower), game.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Horse), game.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Elephant), game.figures()))) == 4
        assert len(list(filter(lambda x: isinstance(x, Queen), game.figures()))) == 2
        assert len(list(filter(lambda x: isinstance(x, King), game.figures()))) == 2
    pass
