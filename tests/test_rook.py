from chemate.board import Board
from chemate.core import Player, Position
from chemate.figures import Rook, Pawn, Knight, Bishop
from chemate.positions import EmptyPosition


class TestRook(object):
    def test_fight_blocked(self):
        board = Board()
        board.init(EmptyPosition())
        rook = Rook(Player.WHITE, Position.from_char('a3'))
        pawn = Pawn(Player.BLACK, Position.from_char('b3'))
        p2 = Knight(Player.WHITE, Position.from_char('a5'))
        bishop = Bishop(Player.BLACK, Position.from_char('h3'))

        board.put_figures([rook, pawn, p2, bishop])

        for movement in board.figure_moves(rook):
            assert movement.to_pos != Position.from_char('a3')
            assert movement.to_pos != Position.from_char('a5')
        pass