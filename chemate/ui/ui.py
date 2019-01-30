from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QFont, QFontDatabase, QDrag, QPainter, QPixmap, QTransform
from PyQt5.QtCore import Qt, QMimeData, QRectF, QLineF, QPointF, QPoint
import chemate.ui.design
from chemate.board import Board, Position
import chemate.figure
import sys


class CellItem(QGraphicsItem):
    def __init__(self, game, position, parent=None):
        self.position = position
        self.game = game
        super().__init__(parent)
        self.cell_size = game.cell_size
        self.setPos((position.index % 8) * self.cell_size, 7*self.cell_size - int(position.index / 8) * self.cell_size)
        self.setAcceptDrops(True)

    def boundingRect(self):
        return QRectF(0, 0, self.cell_size, self.cell_size)

    def paint(self, painter, option, widget=None):
        index = self.position.index
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.white if (index + int(index / 8)) % 2 == 0 else Qt.gray)
        painter.drawRect(self.boundingRect())
        pass

    def dragEnterEvent(self, event):
        all_moves = event.mimeData().legal_moves
        for move in all_moves:
            if move.to_pos == self.position:
                event.setAccepted(True)
                return
        event.setAccepted(False)

    def dragLeaveEvent(self, event):
        super().dragLeaveEvent(event)

    def dropEvent(self, event):
        all_moves = event.mimeData().legal_moves
        for move in all_moves:
            if move.to_pos == self.position:
                self.game.make_move(move)
                """
                to_pos = move.to_pos
                from_pos = move.from_pos

                from_item = self.scene().itemAt(
                    from_pos.x*self.cell_size,
                    7*self.cell_size - from_pos.y*self.cell_size, QTransform())
                to_item = self.scene().itemAt(to_pos.x*self.cell_size, 7*self.cell_size - to_pos.y*64, QTransform())

                if isinstance(to_item, FigureItem):
                    self.scene().removeItem(to_item)
                from_item.setPos(to_pos.x*self.cell_size, 7*self.cell_size - to_pos.y*self.cell_size)

                move.figure.move(move.to_pos)
                """
                return


class FigureItem(QGraphicsItem):
    def __init__(self, game, figure):
        self.cell_size = game.cell_size
        self.figure = figure
        self.font = game.font
        self.figure_char = figure.unicode_char
        super(FigureItem, self).__init__()

        self.setPos(figure.position.x * self.cell_size, self.cell_size * 7 - figure.position.y * self.cell_size)
        self.setCursor(Qt.OpenHandCursor)
        self.setAcceptedMouseButtons(Qt.LeftButton)
        pass

    def paint(self, painter, option, widget=None):
        painter.setFont(self.font)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.drawText(self.boundingRect(), 0, self.figure_char)
        pass

    def boundingRect(self):
        return QRectF(0, 0, self.cell_size, self.cell_size)

    def mouseMoveEvent(self, event):
        if QLineF(
                QPointF(event.screenPos()),
                QPointF(event.buttonDownScreenPos(Qt.LeftButton))
        ).length() < QApplication.startDragDistance():
            return

        legal_moves = [m for m in self.figure.board.legal_moves(self.figure.color) if m.figure == self.figure]
        drag = QDrag(event.widget())
        mime = QMimeData()
        mime.legal_moves = legal_moves

        rect = self.boundingRect()
        pixmap = QPixmap(rect.width(), rect.height())
        pixmap.fill(Qt.white)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        self.paint(painter, None, None)
        painter.end()
        pixmap.setMask(pixmap.createHeuristicMask())

        drag.setPixmap(pixmap)
        drag.setMimeData(mime)
        drag.setHotSpot( QPoint(int(self.cell_size/2), int(self.cell_size/2)))
        drag.exec()

    def mousePressEvent(self, event):
        self.setCursor(Qt.ClosedHandCursor)

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.OpenHandCursor)


class MainWindow(QMainWindow, chemate.ui.design.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.board = None
        self.scene = None
        self.font = None
        self.cell_size = 64

        self.setupUi(self)

        self.actionQuit.triggered.connect(lambda x: sys.exit(0))
        self.actionNewGame.triggered.connect(lambda x: self.new_game())

        self.open_resources()
        self.new_game()

    def open_resources(self):
        fontdb = QFontDatabase()
        font_id = fontdb.addApplicationFont('chess_merida_unicode.ttf')
        families = fontdb.applicationFontFamilies(font_id)
        self.font = QFont(families[0])
        self.font.setPixelSize(self.cell_size-5)

    def init_board(self):
        for i in range(64):
            cell = CellItem(self, Position(i % 8, int(i/8)))
            self.scene.addItem(cell)

        for figure in self.board.figures():
            item = FigureItem(self, figure)
            self.scene.addItem(item)
        pass

    def new_game(self):
        self.board = Board()
        self.board.initial_position()

        self.scene = QGraphicsScene()
        self.viewBoard.setScene(self.scene)
        self.init_board()
        pass

    def make_move(self, move):
        to_pos = move.to_pos
        from_pos = move.from_pos

        from_item = self.scene.itemAt(
            from_pos.x * self.cell_size,
            7 * self.cell_size - from_pos.y * self.cell_size, QTransform())
        to_item = self.scene.itemAt(to_pos.x * self.cell_size, 7 * self.cell_size - to_pos.y * 64, QTransform())

        if isinstance(to_item, FigureItem):
            self.scene.removeItem(to_item)
        from_item.setPos(to_pos.x * self.cell_size, 7 * self.cell_size - to_pos.y * self.cell_size)

        move.figure.move(move.to_pos)


if __name__ == '__main__':
    app = QApplication([])
    view = MainWindow()
    view.show()
    app.exec()
