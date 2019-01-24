import wand.display
import pytest
from chemate.board import Board
from chemate.figure import *
from chemate.image.draw import Draw

# @pytest.mark.skip
def test_display():
    board = Board()
    board.initial_position()
    #fig = Pawn(Player.WHITE, Position('e2'))
    #board.put_figure(fig)

    for fig in filter(lambda x: isinstance(x, Pawn), board.figures()):
        board.board[ fig.position.index ] = None

    #board.make_move(
    #    Position('e2'), Position('e4')
    #)
    draw = Draw()
    for fig in board.figures():
        draw.draw_figure(fig)

    for fig in board.figures():
        for pos in fig.available_moves():
            draw.draw_move_variant(fig.position, pos)

    wand.display.display(draw.image)
