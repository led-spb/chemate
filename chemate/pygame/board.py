import pygame as pg

from chemate.board import Board
from chemate.utils import Position, Player


class BoardCanvas(pg.sprite.Sprite):

    def __init__(self, x: int, y: int, cell_size: int, border: int, *groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.rect = pg.Rect((x, y), (cell_size*8, cell_size*8))
        self.image = pg.Surface((cell_size*8+border, cell_size*8+border))
        pg.draw.rect(self.image, (0, 0, 0), pg.Rect((0, 0), self.image.get_size()))
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
