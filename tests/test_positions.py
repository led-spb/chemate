from chemate.board import Board
from chemate.figures import Bishop, Queen
from chemate.positions import EmptyPosition, PredefinedFENPosition
from chemate.utils import StringPainter
from chemate.core import Position, Player


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


class TestMate:
    def test_mate_1(self):
        board = Board()
        board.init(PredefinedFENPosition('r1bqkbnr/pppp1ppp/8/4p2Q/2B1P3/2K5/PP1P1PPP/n1BK2NR'))
        queen = board.figure_at(Position.from_char('h5'))
        assert isinstance(queen, Queen)
        assert queen.color == Player.WHITE
        moves = list(board.figure_moves(queen))
        assert 'Qh5xf7' in list(map(str, moves))

        move = next(filter(lambda m: str(m) == 'Qh5xf7', moves), None)
        assert move is not None
        board.move(move)
        assert 'Qh5xf7+' == str(move)
