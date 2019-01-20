from chemate.utils import Position


class Figure(object):
    def __init__(self, color, game, position):
        self.color = color
        self.game = game
        self.position = position

    def available_moves(self):
        """
        Get available moves for current figure position
        :return: iterator with valid positions of this figure
        """
        return []

    def move(self, new_position):
        """
        Moving figure to the new position
        :param new_position:
        :return: None
        """
        self.position = new_position


class Pawn(Figure):
    def __init__(self, color, game, position):
        super().__init__(color, game, position)
        self.is_first_move = True

    def direction_move(self):
        return 1 if self.color == 0 else -1

    def available_moves(self):
        # Pawn can move 1 on forward
        new = Position(self.position.x, self.position.y + 1 * self.direction_move())
        if self.game.can_move(color=self.color, position=new, only_empty=True):
            yield new

        # Pawn can move 2 on forward first time
        new = Position(self.position.x, self.position.y + 2 * self.direction_move())
        if self.is_first_move and \
            self.game.can_move(color=self.color, position=new, only_empty=True):
            yield new

        # Pawn can fight only 1 on diagonal
        new = Position(self.position.x + 1, self.position.y + 1 * self.direction_move())
        if self.game.can_move(color=self.color, position=new, only_opposite=True):
            yield new

        new = Position(self.position.x - 1, self.position.y + 1 * self.direction_move())
        if self.game.can_move(color=self.color, position=new, only_opposite=True):
            yield new
        pass

    def move(self, new_position):
        super().move(new_position)
        self.is_first_move = False


class Horse(Figure):

    def available_moves(self):
        all_positions = [
            Position(self.position.x+1, self.position.y+2),
            Position(self.position.x+2, self.position.y+1),
            Position(self.position.x+2, self.position.y-1),
            Position(self.position.x+1, self.position.y-2),

            Position(self.position.x-1, self.position.y-2),
            Position(self.position.x-2, self.position.y-1),
            Position(self.position.x-2, self.position.y+1),
            Position(self.position.x-1, self.position.y+2)
        ]
        for new in all_positions:
            if self.game.can_move(color=self.color, position=new):
                yield new
        pass


class Elephant(Figure):
    pass


class Tower(Figure):
    pass


class Queen(Figure):
    pass


class King(Figure):
    pass

