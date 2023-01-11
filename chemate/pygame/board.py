import pygame as pg


class BoardSprite(pg.sprite.Sprite):

    def __init__(self, x: int, y: int, cell_size: int, border: int, *groups: pg.sprite.AbstractGroup) -> None:
        super().__init__(*groups)
        self.rect = pg.Rect((x, y), (cell_size*8, cell_size*8))
        self.image = pg.Surface((cell_size*8+border, cell_size*8+border))
        pg.draw.rect(self.image, (0, 0, 0), pg.Rect((0, 0), self.image.get_size()))

        for y in range(8):
            for x in range(8):
                index = x + y*8
                color = (140, 140, 140) if (index + int(index / 8)) % 2 == 0 else (255, 255, 255)
                pg.draw.rect(self.image, color,
                             pg.Rect(x * cell_size + border, y * cell_size + border,
                                     cell_size-border, cell_size-border))
        pass
