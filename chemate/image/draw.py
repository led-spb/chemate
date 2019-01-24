from chemate.board import Board
from chemate.utils import Position
from chemate.board import Movement
from wand.image import Image
from wand.font import Font
from wand.drawing import Drawing
from wand.color import Color


class Draw(object):

    def __init__(self, cell_size=32):
        self.cell_size = cell_size
        self.drw = Drawing()
        self.draw_cells()
        self.unichars = dict(
            zip("KQRBNPkqrbnp",
                (chr(uc) for uc in range(0x2654, 0x2660)))
        )

    @property
    def image(self):
        _image = Image(
            width=self.cell_size*8,
            height=self.cell_size*8,
        )
        self.drw.draw(_image)
        return _image

    def draw_cells(self):
        for i in range(64):
            self.drw.fill_color = Color('white') if (i + int(i/8)) % 2 == 0 else Color('grey')
            self.drw.rectangle(
                left=(i % 8) * self.cell_size,
                top=int(i / 8) * self.cell_size,
                width=self.cell_size,
                height=self.cell_size
            )
        self.drw.push()

    def draw_figure(self, figure):
        self.drw.font = './chess_merida_unicode.ttf'
        self.drw.font_size = self.cell_size

        self.drw.fill_color = Color('black')

        self.drw.text(
            figure.position.x * self.cell_size,
            8*self.cell_size - figure.position.y*self.cell_size - 6,
            self.unichars[figure.char]
        )
        self.drw.push()
        pass

    def draw_move_variant(self, from_pos, to_pos):
        self.drw.fill_color = Color('black')
        self.drw.line(
            (from_pos.x * self.cell_size + int(self.cell_size/2),
             8*self.cell_size - from_pos.y*self.cell_size - int(self.cell_size/2)),

            (to_pos.x * self.cell_size + int(self.cell_size/2),
             8*self.cell_size - to_pos.y*self.cell_size - int(self.cell_size/2))
        )
        self.drw.push()

    def draw_estimate(self, pos, score):
        self.drw.fill_color = Color('black')
        self.drw.font = 'Verdana'
        self.drw.font_size = 10
        self.drw.text(pos.x * self.cell_size,
                      8*self.cell_size - pos.y*self.cell_size,
                      '%.1f' % score
        )

    def draw_board(self, board):
        for fig in board.figures():
            self.draw_figure(fig)