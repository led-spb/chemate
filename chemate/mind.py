from chemate.board import Board


class Estimate(object):
    def __init__(self, color, board, level, max_level):
        self.color = color
        self.level = level
        self.max_level = max_level
        self.estimates = []
        pass

    def make_move(self, board, color):
        """
        Main method for computer chess
        :return: None
        """
        # 1. Generate all available moves for current position
        for figure in filter(lambda x: x.color == color, board.figures()):
            for new_position in figure.available_moves():
                # 2. Make a move and start calculate estimate
                new_board = self.board.copy()
                new_board.move_figure(figure.position, new_position)

                self.estimates.append(
                    Estimate(color, board, self.level+1, self.max_level)
                )
                pass
        pass
