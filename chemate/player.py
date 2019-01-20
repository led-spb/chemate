class Player(object):
    WHITE = 0
    BLACK = 1

    def __init__(self, game, color, name):
        self.game = game
        self.color = color
        self.name = name

    def figures(self):
        """
        Get all figures, owned by the player
        :return:
        """
        return filter(lambda item: item.color == self.color, self.game.figures())
