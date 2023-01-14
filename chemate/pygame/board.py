from typing import Union

import pygame as pg

from chemate.board import Board
from chemate.utils import Position, Player


class BoardSprite(pg.sprite.Sprite):
    def __init__(self, rect: pg.Rect, board_border: int, cell_size: int):
        super().__init__()
        self.rect = rect
        self.image = pg.Surface(rect.size)
        pg.draw.rect(self.image, (55, 10, 7), pg.Rect((0, 0), rect.size))
        font = pg.font.SysFont('Verdana', board_border, True)
        self.draw_numbers(font, board_border, cell_size)

    def draw_numbers(self, font, border, cell_size):
        for idx, char in enumerate("ABCDEFGH"):
            img = font.render(char, True, (255, 255, 255))
            img.set_alpha(128)
            x = border+idx*cell_size+(cell_size-img.get_width())//2
            self.image.blit(img, (x, (self.rect.height-img.get_height())))

        for idx, char in enumerate("87654321"):
            img = font.render(char, True, (255, 255, 255))
            img.set_alpha(128)
            y = border+idx*cell_size+(cell_size-img.get_height())//2
            self.image.blit(img, ((border-img.get_width())//2, y))
        pass


class CellItem(pg.sprite.Sprite):
    def __init__(self, font: pg.font.Font, x: int, y: int, cell_size: int, position: Position, board: Board) -> None:
        super().__init__()
        self.font = font
        self.board = board
        self.highlighted = False
        self.position = position
        self.rect = pg.Rect((x, y), (cell_size, cell_size))
        self.image = pg.Surface((cell_size, cell_size))
        self.color = (255, 255, 255) if self.position.color == Player.WHITE else (140, 140, 140)
        self.highlight_surface = pg.Surface((cell_size, cell_size))
        self.highlight_surface.set_alpha(64)
        pg.draw.rect(self.highlight_surface, (0, 255, 0), pg.Rect((0, 0), self.highlight_surface.get_size()))

    def update(self) -> None:
        pg.draw.rect(self.image, self.color, pg.Rect((0, 0), self.image.get_size()))
        figure = self.board.get_figure(self.position)
        if figure is not None:
            img = self.font.render(figure.unicode_char, True, (0, 0, 0))
            self.image.blit(img, (0, 0))
        if self.highlighted:
            self.image.blit(self.highlight_surface, (0, 0))
        pass


class BoardCanvas(pg.sprite.Group):

    def __init__(self, font: pg.font.Font, board: Board, pos: tuple[int, int], cell_size: int,
                 *groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.board_border = 15
        self.cell_size = cell_size
        self.cell_border = 2
        self.rect = pg.Rect(
            pos,
            (self.board_border*2+self.cell_size*8+self.cell_border,
             self.board_border*2+self.cell_size*8+self.cell_border)
        )
        self.board_spite = BoardSprite(self.rect, self.board_border, self.cell_size)
        self.cells = pg.sprite.Group()
        self.make_cells(board, font)

        self.add(self.board_spite, self.cells)
        pass

    def find_cell(self, pos: tuple[int, int]) -> Union[CellItem, None]:
        for cell in self.cells.sprites():
            if cell.rect.collidepoint(pos):
                return cell
        return None

    def make_cells(self, board: Board, font: pg.font.Font):
        for pos in [Position(i) for i in range(64)]:
            cell = CellItem(font,
                            self.rect.left + self.board_border + self.cell_border // 2 + pos.x * self.cell_size +
                            self.cell_border // 2,
                            self.rect.top + self.board_border + self.cell_border // 2 + (
                                        7 - pos.y) * self.cell_size + self.cell_border // 2,
                            self.cell_size - self.cell_border,
                            pos, board)
            self.cells.add(cell)
