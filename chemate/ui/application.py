from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsItem
from PyQt5.QtGui import QFont, QFontDatabase, QDrag, QPainter, QPixmap, QTransform
from PyQt5.QtCore import Qt, QMimeData, QRectF, QLineF, QPointF, QPoint, QThread
import chemate.ui.design
from chemate.positions import InitialPosition
from chemate.utils import Position, Player
from chemate.board import Board
from chemate.decision import DecisionTree
import sys


class DecisionThread(QThread):
    def __init__(self, decision, color, parent=None):
        super().__init__(parent)
        self.decision = decision
        self.color = color
        self.move = None
        self.score = None

    def run(self):
        try:
            self.move, self.score = self.decision.best_move(self.color)
        except Exception as err:
            print(err)


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
                return


class FigureItem(QGraphicsItem):
    def __init__(self, game, figure):
        self.cell_size = game.cell_size
        self.game = game
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
        distance = QLineF(QPointF(event.screenPos()),
                QPointF(event.buttonDownScreenPos(Qt.LeftButton))
        ).length()
        if distance < QApplication.startDragDistance() \
                or self.figure.color != self.game.human \
                or self.game.turn != self.game.human:
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


class GameWindow(QMainWindow, chemate.ui.design.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.board = None
        self.scene = None
        self.font = None
        self.human = Player.WHITE
        self.turn = Player.WHITE
        self.cell_size = 64
        self.decision = None

        self.setupUi(self)

        self.actionQuit.triggered.connect(lambda x: sys.exit(0))
        self.actionNewGame.triggered.connect(lambda x: self.new_game())
        self.actionRollbackMove.triggered.connect(lambda x: self.rollback_move())

        self.open_resources()
        self.new_game()

    def open_resources(self):
        fontdb = QFontDatabase()
        font_id = fontdb.addApplicationFont('chess_merida_unicode.ttf')
        families = fontdb.applicationFontFamilies(font_id)
        self.font = QFont(families[0])
        self.font.setPixelSize(self.cell_size-5)

    def init_board(self):
        self.scene.clear()
        for i in range(64):
            cell = CellItem(self, Position(i % 8, int(i/8)))
            self.scene.addItem(cell)

        for figure in self.board.figures():
            item = FigureItem(self, figure)
            self.scene.addItem(item)
        pass

    def new_game(self):
        self.board = Board(InitialPosition())

        self.scene = QGraphicsScene()
        self.viewBoard.setScene(self.scene)
        self.turn = Player.WHITE
        self.decision = DecisionTree(board=self.board, max_level=2)

        self.init_board()
        pass

    def make_move(self, movement):
        """
        :type movement: Movement
        """
        self.statusbar.showMessage(str(movement))
        to_pos = movement.to_pos
        from_pos = movement.from_pos

        from_item = self.scene.itemAt(
            from_pos.x * self.cell_size,
            7 * self.cell_size - from_pos.y * self.cell_size, QTransform())
        to_item = self.scene.itemAt(to_pos.x * self.cell_size, 7 * self.cell_size - to_pos.y * 64, QTransform())

        if isinstance(to_item, FigureItem):
            self.scene.removeItem(to_item)
        from_item.setPos(to_pos.x * self.cell_size, 7 * self.cell_size - to_pos.y * self.cell_size)

        self.board.make_move(movement)
        self.turn = -self.turn
        if self.board.has_mate(self.turn):
            result = 'LOOSE' if self.turn == self.human else 'WIN'
            print('You %s!' % result)
            self.statusbar.showMessage(result)
            return

        # When movement is transform pawn or rook, need to build new scene
        if movement.transform_to is not None or movement.rook is not None:
            self.init_board()

        if self.turn != self.human:
            self.start_think(self.turn)

    def rollback_move(self):
        if self.turn != self.human:
            return

        self.board.rollback_move()
        self.board.rollback_move()
        self.init_board()
        pass

    def start_think(self, color):
        self.think_thread = DecisionThread(self.decision, color)
        self.think_thread.finished.connect(self.think_done)
        self.think_thread.start()
        pass

    def think_done(self):
        print("Think done, score: %.2f" % self.think_thread.score)
        if self.think_thread.move is not None:
            self.make_move(self.think_thread.move)
        pass


def main():
    app = QApplication([])
    view = GameWindow()
    view.show()
    try:
        app.exec()
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
