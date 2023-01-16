from chemate.board import Board
from chemate.core import Player, Position
from chemate.figures import Knight
from chemate.positions import EmptyPosition


class TestKnight(object):
    def test_move(self):
        board = Board()
        board.init(EmptyPosition())
        knight = Knight(Player.BLACK, Position.from_char('d5'))
        board.put_figure(knight)

        idx = 0
        for idx, move in enumerate(board.figure_moves(knight)):
            board.move(move)
            assert len(board.moves) == 1
            board.rollback()
            assert len(board.moves) == 0
        assert idx == 7
