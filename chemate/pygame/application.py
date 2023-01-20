import importlib.resources
import queue

import pygame as pg
import pygame_gui as gui

from .board import BoardCanvas
from ..board import Board
from ..decision import DecisionTree
from ..positions import InitialPosition
from ..core import Player, Movement
from multiprocessing import Process, Queue


def decision_process(queue: Queue, result: Queue):
    print('decision process started')
    decision = DecisionTree(4)
    while True:
        board = queue.get()
        move, score, variants = decision.best_move(board)
        # print(f'Best move {move}. score {score}. variants: {variants}')
        result.put(move)
    pass


class Application:
    def __init__(self):
        pg.init()
        self.cell_size = 64
        self.cell_border = 2
        self.FPS = 15
        self.outer_border = 15
        self.running = False
        self.clock = pg.time.Clock()
        self.screen = None
        self.static = pg.sprite.Group()
        self.board = Board()
        self.board.init(InitialPosition())
        self.human_players = (Player.WHITE,)
        self.selected_figure = None
        self.valid_moves = []

        pg.display.set_caption('Chemate')

        pg.font.init()
        figure_font = pg.font.Font(
            importlib.resources.path(__package__, 'chess_merida_unicode.ttf'), self.cell_size
        )

        # Make board canvas
        self.board_canvas = BoardCanvas(
            board=self.board,
            font=figure_font,
            pos=(self.outer_border, self.outer_border),
            cell_size=self.cell_size
        )
        self.static.add(self.board_canvas)

        self.task_queue = Queue()
        self.result_queue = Queue()
        self.ai_process = Process(
            target=decision_process,
            kwargs={'queue': self.task_queue, 'result': self.result_queue}
        )

        self.WIDTH = self.outer_border * 2 + self.board_canvas.rect.width
        self.HEIGHT = self.outer_border * 2 + self.board_canvas.rect.height
        self.gui_manager = gui.UIManager((self.WIDTH, self.HEIGHT))
        # self.make_gui()
        pass

    def make_gui(self):
        welcome_wnd = gui.elements.UIWindow(
            rect=pg.Rect((0, 0), (self.WIDTH, self.HEIGHT)), resizable=True, draggable=True,
            window_display_title="Welcome",
            manager=self.gui_manager
        )
        text_output_box = gui.elements.UITextBox(
            relative_rect=pg.Rect((0, 0), welcome_wnd.get_container().get_size()),
            html_text="<b>Welcome to Chess game!</b>",
            container=welcome_wnd)
        pass

    def start_comp_move(self):
        self.task_queue.put(self.board)

    def process_comp_move(self):
        if self.board.current in self.human_players or self.ai_process is None:
            return
        try:
            move = self.result_queue.get(False)
            if move is not None:
                self.make_move(move)
        except queue.Empty:
            pass
        return

    def make_move(self, move: Movement):
        self.board.move(move)
        if self.board.current == Player.WHITE:
            print(f"{self.board.move_number}. {move}", end="\t")
        else:
            print(f'{move}')

        self.selected_figure = None
        self.valid_moves = []
        if self.board.current not in self.human_players:
            self.start_comp_move()
        # clear highlight
        for cell in self.board_canvas.cells:
            cell.highlighted = False
        pass

    def on_click(self, pos):
        if self.board.current not in self.human_players:
            return

        cell = self.board_canvas.find_cell(pos)
        if cell is None:
            return
        position = cell.position
        figure = self.board.figure_at(position)
        if figure is not None and figure.color == self.board.current:
            self.selected_figure = figure
            self.valid_moves = list(self.board.figure_moves(figure))
            highlighted = [move.to_pos for move in self.valid_moves] + [self.selected_figure.position]
            for cell in self.board_canvas.cells:
                cell.highlighted = cell.position in highlighted
            return

        if self.selected_figure is not None:
            for move in self.valid_moves:
                if move.to_pos == position:
                    self.make_move(move)
                    return
        pass

    def rollback_move(self):
        if self.board.current not in self.human_players:
            return
        self.board.rollback()
        self.board.rollback()
        for cell in self.board_canvas.cells:
            cell.highlighted = False
        pass

    def run(self):
        self.ai_process.start()
        try:
            self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
            self.running = True

            timedelta = 0
            while self.running:
                self.static.update()
                self.screen.fill((0, 0, 0))
                self.static.draw(self.screen)
                self.process_comp_move()

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                    if event.type == pg.MOUSEBUTTONUP:
                        self.on_click(event.pos)
                    if event.type == pg.KEYDOWN:
                        if event.key == 122 and event.mod & pg.KMOD_CTRL:
                            self.rollback_move()
                    self.gui_manager.process_events(event)

                self.gui_manager.update(timedelta/1000.0)
                self.gui_manager.draw_ui(self.screen)

                pg.display.flip()
                timedelta = self.clock.tick(self.FPS)
        finally:
            self.ai_process.kill()
        pass
