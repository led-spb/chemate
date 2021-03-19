from chemate.figure import Bishop
from chemate.positions import EmptyPosition, PredefinedFENPosition
from chemate.utils import Player


class TestEmptyPositions:
    def test_figures(self):
        factory = EmptyPosition()
        assert list(factory.figures()) == []


class TestFENPosition:
    def test_figures(self):
        factory = PredefinedFENPosition('8/8/8/8/8/8/8/8')
        assert list(factory.figures()) == []

        figures = list(PredefinedFENPosition('8/8/8/3B/8/8/8/8').figures())
        assert len(figures) == 1
        assert isinstance(figures[0], Bishop) and figures[0].color == Player.WHITE and str(figures[0].position) == 'd5'

        factory = PredefinedFENPosition('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        assert len(list(factory.figures())) == 32