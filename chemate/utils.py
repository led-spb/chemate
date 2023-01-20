import re
from abc import abstractmethod

from chemate.core import Player, Position


class BoardExporter:
    def __init__(self, board):
        self.board = board

    @abstractmethod
    def export(self) -> str:
        ...


class PlainExporter(BoardExporter):

    def export(self) -> str:
        lines = [['.' for x in range(8)] for y in range(8)]
        for figure in self.board.figures:
            lines[7 - figure.position.y][figure.position.x] = figure.char
        return "\n".join([" ".join(line) for line in lines])


class FENExporter(BoardExporter):
    def export(self) -> str:
        data = []
        for y in range(8):
            row = [self.board.board[y*8+x].char if self.board.board[y*8+x] is not None else '0' for x in range(8)]
            data.insert(0,
                        re.sub(r"0+", lambda m: str(len(m.group(0))), "".join(row)))
        position = "/".join(data)
        return f"{position} {'w' if self.board.current == Player.WHITE else 'b'} " \
               f"{'K' if self.rook_avail(Player.WHITE, False) else '-'}" \
               f"{'Q' if self.rook_avail(Player.WHITE, True) else '-'}" \
               f"{'k' if self.rook_avail(Player.BLACK, False) else '-'}" \
               f"{'q' if self.rook_avail(Player.BLACK, True) else '-'}" \
               f" - 0 {self.board.move_number}"

    def rook_avail(self, color: int, long: bool) -> bool:
        king = self.board.figure_at(Position.from_xy(4, 0 if color == Player.WHITE else 7))
        rook = self.board.figure_at(Position.from_xy(0 if long else 7, 0 if color == Player.WHITE else 7))
        return king is not None and king.color == color and king.moves == 0 and \
            rook is not None and rook.color == color and rook.moves == 0
