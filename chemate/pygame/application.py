import importlib.resources
import queue

import pygame as pg

from .board import BoardCanvas, CellItem
from ..board import Board
from ..decision import DecisionTree
from ..positions import InitialPosition
from ..utils import Player, Position, Movement
from multiprocessing import Process, Queue


def decision_process(queue: Queue, result: Queue, color: int):
    print('decision process started')
    while True:
        board = queue.get()
        decision = DecisionTree(board, 2)
        move, score = decision.best_move(color)
        result.put(move)
    return


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
        self.board = Board(InitialPosition())
        self.human_player = Player.WHITE
        self.current_player = Player.WHITE
        self.selected_figure = None
        self.valid_moves = []

        pg.display.set_caption('Chemate')

        pg.font.init()
        figure_font = pg.font.Font(
            importlib.resources.path(__package__, 'chess_merida_unicode.ttf'), self.cell_size
        )

        # Make board canvas
        BoardCanvas(self.outer_border, self.outer_border, self.cell_size, self.cell_border, self.static)

        # Create board cells
        self.cells = pg.sprite.Group()
        for pos in [Position(i) for i in range(64)]:
            cell = CellItem(figure_font,
                            self.outer_border+self.cell_border//2 + pos.x*self.cell_size+self.cell_border//2,
                            self.outer_border+self.cell_border//2 + (7 - pos.y)*self.cell_size+self.cell_border//2,
                            self.cell_size-self.cell_border,
                            pos, self.board)
            self.cells.add(cell)
        self.static.add(self.cells)

        self.task_queue = Queue()
        self.result_queue = Queue()
        self.ai_process = Process(
            target=decision_process,
            kwargs={'color': self.human_player * -1,
                    'queue': self.task_queue,
                    'result': self.result_queue}
        )
        pass

    def start_comp_move(self):
        self.task_queue.put(self.board)

    def process_comp_move(self):
        if self.current_player == self.human_player or self.ai_process is None:
            return
        try:
            move = self.result_queue.get(False)
            if move is not None:
                self.make_move(move)
        except queue.Empty:
            pass
        return

    def make_move(self, move: Movement):
        self.board.make_move(move)
        print(f"{len(self.board.moves)}. {move}")
        self.selected_figure = None
        self.current_player = self.current_player * -1
        self.valid_moves = []
        if self.current_player != self.human_player:
            self.start_comp_move()
        # clear highlight
        for cell in self.cells.sprites():
            cell.highlighted = False
        pass

    def on_click(self, pos):
        if self.current_player != self.human_player:
            return

        position = None
        for cell in self.cells.sprites():
            if cell.rect.collidepoint(pos):
                position = cell.position
                break
        if position is None:
            return

        figure = self.board.get_figure(position)
        if figure is not None and figure.color == self.current_player:
            self.selected_figure = figure
            self.valid_moves = self.board.legal_moves(self.current_player, figure)
            highlighted = [move.to_pos for move in self.valid_moves] + [self.selected_figure.position]
            for cell in self.cells.sprites():
                cell.highlighted = cell.position in highlighted
            return

        if self.selected_figure is not None:
            for move in self.valid_moves:
                if move.to_pos == position:
                    self.make_move(move)
                    return
        pass

    def run(self):
        self.ai_process.start()
        try:
            self.screen = pg.display.set_mode([self.WIDTH, self.HEIGHT])
            self.running = True

            while self.running:
                self.static.update()
                self.screen.fill((220, 220, 220))
                self.static.draw(self.screen)
                self.process_comp_move()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                    if event.type == pg.MOUSEBUTTONUP:
                        self.on_click(event.pos)

                pg.display.flip()
                self.clock.tick(self.FPS)
        finally:
            self.ai_process.kill()
        pass
