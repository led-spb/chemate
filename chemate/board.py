from typing import Iterator, Union

from chemate.figures import King, Pawn, Queen, Rook, Bishop, Knight
from chemate.positions import PositionFactory
from chemate.core import Position, Movement, Figure, Player
from chemate.directions import Left, Right


class Board:
    def __init__(self) -> None:
        self.board = []
        self.moves = []
        self.balance = 0
        self.clear()

    def clear(self) -> None:
        self.board = [None for x in range(64)]
        self.moves = []
        self.balance = 0

    def init(self, factory: PositionFactory) -> None:
        self.clear()
        self.put_figures(factory.figures())

    def put_figures(self, figures: Iterator[Figure]) -> None:
        for figure in figures:
            self.put_figure(figure)
        pass

    def __str__(self):
        lines = [['.' for x in range(8)] for y in range(8)]
        for figure in self.figures:
            lines[7 - figure.position.y][figure.position.x] = figure.char
        return "\n".join([" ".join(line) for line in lines])

    def put_figure(self, figure: Figure) -> None:
        self.board[figure.position.index] = figure
        self.balance += figure.price

    def remove_figure(self, figure: Figure) -> None:
        self.board[figure.position.index] = None
        self.balance -= figure.price

    def attacked_by(self, figure: Figure) -> Iterator[Position]:
        for direction in figure.directions(True):
            for pos in direction:
                fig = self.figure_at(pos)
                if fig is not None and fig.color == figure.color:
                    break
                yield pos
                if fig is not None:
                    break
        pass

    def is_attacked(self, color: int, position: Position) -> bool:
        for figure in self.board:
            if figure is None or figure.color == color:
                continue
            if position in self.attacked_by(figure):
                return True
        return False

    @property
    def last_move(self) -> Union[Movement, None]:
        if len(self.moves) > 0:
            return self.moves[-1]
        return None

    @property
    def figures(self) -> Iterator[Figure]:
        for figure in self.board:
            if figure is not None:
                yield figure
        pass

    def figure_at(self, position: Position) -> Union[None, Figure]:
        return self.board[position.index]

    def figure_by_class(self, kind, color: int = None) -> Iterator[Figure]:
        for figure in self.board:
            if figure is not None and (color is None or figure.color == color) and isinstance(figure, kind):
                yield figure
        pass

    def valid_moves(self, color: int) -> Iterator[Movement]:
        for figure in self.figures:
            if figure.color == color:
                yield from self.figure_moves(figure)
        pass

    def figure_moves(self, figure: Figure) -> Iterator[Movement]:
        is_pawn = isinstance(figure, Pawn)
        is_king = isinstance(figure, King)

        for direction in figure.directions():
            for pos in direction:
                taken_figure = self.figure_at(pos)
                rook = None
                transform_to = [None]

                if taken_figure is not None and taken_figure.color == figure.color:
                    break

                if is_pawn:
                    if figure.position.x == pos.x and taken_figure is not None:
                        break

                    if figure.position.x != pos.x and taken_figure is None:
                        if not (pos.y == 5 and figure.color == Player.WHITE) and \
                                not (pos.y == 2 and figure.color == Player.BLACK):
                            break
                        passthrough_pos = Position(pos.index + (-8 if figure.color == Player.WHITE else +8))
                        taken_figure = self.figure_at(passthrough_pos)
                        if taken_figure is None or not isinstance(taken_figure, Pawn) or \
                                taken_figure.color == figure.color:
                            break
                        if self.last_move is None or self.last_move.figure != taken_figure or \
                                abs(self.last_move.from_pos.index - self.last_move.to_pos.index) != 16:
                            break

                if is_pawn and pos.is_last_line_for(figure.color):
                    transform_to = [
                        Queen(figure.color, pos), Rook(figure.color, pos), Bishop(figure.color, pos),
                        Knight(figure.color, pos)
                    ]

                # King rooking logic
                if is_king and abs(pos.index-figure.position.index) == 2:
                    rook_valid, rook = self.validate_rooking(figure, pos)
                    if not rook_valid:
                        break

                for transform in transform_to:
                    move = Movement(
                        figure=figure,
                        from_pos=figure.position,
                        to_pos=pos,
                        taken_figure=taken_figure,
                        transform_to=transform,
                        rook=rook
                    )
                    self.move(move, test_mode=True)
                    has_check = self.test_for_check(figure.color)
                    self.rollback()
                    if has_check:
                        break
                    yield move
                if taken_figure is not None:
                    break
        pass

    def validate_rooking(self, king: Figure, pos: Position) -> tuple[bool, Union[Figure, None]]:
        is_long = (pos.index - king.position.index) < 0
        rook = self.figure_at(Position.from_xy(0 if is_long else 7, pos.y))

        if rook is None or not isinstance(rook, Rook) or king.color != rook.color or rook.moves > 0:
            return False, rook

        rook_direction = Left(king.position, 3) if is_long else Right(king.position, 2)
        for figure in map(self.figure_at, rook_direction):
            if figure is not None:
                return False, rook

        for delta in range(0, -3 if is_long else +3, -1 if is_long else 1):
            if self.is_attacked(king.color, Position(king.position.index+delta)):
                return False, rook
        return True, rook

    def move(self, movement: Movement, test_mode: bool = False) -> None:
        if movement.taken_figure is not None:
            self.remove_figure(movement.taken_figure)

        self.board[movement.from_pos.index] = None
        self.board[movement.to_pos.index] = movement.transform_to or movement.figure

        movement.figure.position = movement.to_pos
        movement.figure.moves += 1

        if movement.rook is not None:
            is_long = movement.to_pos.index - movement.from_pos.index < 0
            rook_pos = Position(movement.to_pos.index + (1 if is_long else -1))
            self.board[movement.rook.position.index] = None
            self.board[rook_pos.index] = movement.rook
            movement.rook.position = rook_pos
            movement.rook.moves += 1

        self.moves.append(movement)

        if not test_mode:
            movement.is_check = self.test_for_check(movement.figure.color * -1)
        pass

    def rollback(self) -> None:
        if len(self.moves) == 0:
            return

        move = self.moves.pop()

        self.board[move.to_pos.index] = None
        self.board[move.from_pos.index] = move.figure
        move.figure.position = move.from_pos
        move.figure.moves -= 1

        if move.rook is not None:
            is_long = move.to_pos.index - move.from_pos.index < 0
            initial_pos = Position(move.to_pos.index + (-2 if is_long else 1))
            self.board[move.rook.position.index] = None
            self.board[initial_pos.index] = move.rook
            move.rook.position = initial_pos
            move.rook.moves -= 1

        if move.taken_figure is not None:
            self.put_figure(move.taken_figure)
        pass

    def test_for_check(self, color: int) -> bool:
        king = next(self.figure_by_class(King, color), None)
        if king is None:
            # raise ValueError('King is not found on the board')
            return False
        return self.is_attacked(king.color, king.position)

    def test_for_mate(self, color: int) -> bool:
        return self.test_for_check(color) and len(list(self.valid_moves(color))) == 0
