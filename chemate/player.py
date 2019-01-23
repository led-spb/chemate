class Player(object):
    WHITE = 1
    BLACK = -1

    def __init__(self, board, color, name):
        self.board = board
        self.color = color
        self.name = name

    def figures(self):
        """
        Get all figures, owned by the player
        :return:
        """
        return filter(lambda item: item.color == self.color, self.board.figures())

    def make_move(self):
        pass
