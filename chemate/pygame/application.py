import importlib.resources
import pygame as pg
from .board import BoardSprite
from ..board import Board
from ..figure import Queen
from ..positions import InitialPosition
from ..utils import Player, Position


class Application:
    def __init__(self):
        pg.init()
        self.cell_size = 64
        self.cell_border = 2
        self.FPS = 15
        self.outer_border = 15
        self.WIDTH = self.cell_size * 8 + self.outer_border * 2 + self.cell_border
        self.HEIGHT = self.cell_size * 8 + self.outer_border * 2 + self.cell_border
        self.running = False
        self.clock = pg.time.Clock()
        self.screen = None
        self.static = pg.sprite.Group()
        self.figures = pg.sprite.Group()
        self.board = Board(InitialPosition())
        self.current_player = Player.WHITE
        self.selected_figure = None
        self.valid_moves = []

        pg.display.set_caption('Chemate')
        pg.font.init()
        self.figure_font = pg.font.Font(
            importlib.resources.path(__package__, 'chess_merida_unicode.ttf'), self.cell_size)
        BoardSprite(self.outer_border, self.outer_border, self.cell_size, self.cell_border, self.static)

    def draw_board(self):
        self.screen.fill((220, 220, 220))
        self.static.draw(self.screen)

    def highlight_cell(self, pos: Position):
        pg.draw.rect(self.screen, (0, 128, 0, 100), pg.Rect(
            self.outer_border + pos.x * self.cell_size + self.cell_border,
            self.outer_border + (7 - pos.y) * self.cell_size + self.cell_border,
            self.cell_size - self.cell_border, self.cell_size - self.cell_border
        ))

    def draw(self):
        if self.selected_figure is not None:
            position = self.selected_figure.position
            self.highlight_cell(position)
        for move in self.valid_moves:
            self.highlight_cell(move.to_pos)

        for figure in self.board.figures():
            img = self.figure_font.render(figure.unicode_char, True, (0, 0, 0))
            self.screen.blit(
                img,
                (self.outer_border + figure.position.x * self.cell_size + self.cell_border // 2,
                 self.outer_border + (7-figure.position.y) * self.cell_size + self.cell_border // 2)
            )
            pass
        pass

    def on_click(self, pos):
        x = (pos[0] - self.outer_border) // self.cell_size
        y = 7 - (pos[1] - self.outer_border) // self.cell_size
        position = Position.from_xy(x, y)
        figure = self.board.get_figure(position)

        if figure is not None and figure.color == self.current_player:
            self.selected_figure = figure
            self.valid_moves = self.board.legal_moves(self.current_player, figure)
            return

        if self.selected_figure is not None:
            for move in self.valid_moves:
                if move.to_pos == position:
                    self.board.make_move(move)
                    self.selected_figure = None
                    self.valid_moves = []
                    self.current_player = self.current_player * -1
                    return
        pass

    def run(self):
        self.screen = pg.display.set_mode([self.WIDTH, self.HEIGHT])
        self.running = True
        self.draw_board()

        q = Queen(Player.BLACK, Position.from_char('a8'))
        img = self.figure_font.render(q.unicode_char, True, (255, 255, 255))
        self.screen.blit(img, (self.outer_border+self.cell_border//2, self.outer_border+self.cell_border//2))

        while self.running:
            self.draw_board()
            self.draw()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                if event.type == pg.MOUSEBUTTONUP:
                    self.on_click(event.pos)

            pg.display.flip()
            self.clock.tick(self.FPS)
