from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsItemGroup
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
import chemate.ui.design
from chemate.board import Board
import sys


class MainWindow(QMainWindow, chemate.ui.design.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.unichars = dict(
            zip("KQRBNPkqrbnp",
                (chr(uc) for uc in range(0x2654, 0x2660)))
        )
        self.cell_size = 64

        self.setupUi(self)
        self.actionQuit.triggered.connect(lambda x: sys.exit(0))
        self.actionNewGame.triggered.connect(lambda x: self.new_game())
        self.board = None

        self.fontdb = QFontDatabase()
        font_id = self.fontdb.addApplicationFont('chess_merida_unicode.ttf')
        families = self.fontdb.applicationFontFamilies(font_id)
        self.font = QFont(families[0])
        self.font.setPixelSize(self.cell_size-5)

        self.scene = QGraphicsScene()
        self.group_board = QGraphicsItemGroup()
        self.group_figures = QGraphicsItemGroup()

        self.scene.addItem(self.group_board)
        self.scene.addItem(self.group_figures)

        self.viewBoard.setScene(self.scene)

        self.init_board()
        self.new_game()

    def draw_board(self):
        for figure in self.board.figures():
            item = self.scene.addText(
                self.unichars[figure.char], font=self.font
            )
            item.setPos(figure.position.x * self.cell_size, self.cell_size*7 - figure.position.y*self.cell_size)
            self.group_figures.addToGroup(item)
        pass

    def new_game(self):
        self.board = Board()
        self.board.initial_position()
        for item in self.group_figures.childItems():
            self.group_figures.removeFromGroup(item)
        self.draw_board()
        pass

    def init_board(self):
        for i in range(64):
            fill_color = Qt.white if (i + int(i/8)) % 2 == 0 else Qt.gray
            self.group_board.addToGroup(
                self.scene.addRect(
                    (i % 8) * self.cell_size,
                    int(i / 8) * self.cell_size,
                    self.cell_size, self.cell_size, brush=fill_color
                )
            )
        pass


if __name__ == '__main__':
    app = QApplication([])
    view = MainWindow()
    view.show()
    app.exec()
