from typing import Iterator

from chemate.directions import Up, Down, Left, Right, UpRight, UpLeft, DownRight, DownLeft
from chemate.core import Position, Player, Figure, Direction


class Pawn(Figure):
    _price = 1
    _char = 'p'

    def directions(self, attack: bool = False) -> Iterator[Direction]:
        if self.color == Player.WHITE:
            yield UpRight(self.position, limit=1)
            yield UpLeft(self.position, limit=1)
        else:
            yield DownRight(self.position, limit=1)
            yield DownLeft(self.position, limit=1)

        if not attack:
            if self.color == Player.WHITE:
                yield Up(self.position, limit=2 if self.position.y == 1 else 1)
            else:
                yield Down(self.position, limit=2 if self.position.y == 6 else 1)
        pass


class Bishop(Figure):
    _price = 3
    _char = 'b'

    def directions(self, attack: bool = False) -> Iterator[Direction]:
        yield UpLeft(self.position)
        yield UpRight(self.position)
        yield DownLeft(self.position)
        yield DownRight(self.position)


class Knight(Figure):
    _price = 3
    _char = 'n'

    def directions(self, attack: bool = False) -> Iterator[Direction]:
        all_positions = [
            (self.position.x + 1, self.position.y + 2),
            (self.position.x + 2, self.position.y + 1),
            (self.position.x + 2, self.position.y - 1),
            (self.position.x + 1, self.position.y - 2),
            (self.position.x - 1, self.position.y - 2),
            (self.position.x - 2, self.position.y - 1),
            (self.position.x - 2, self.position.y + 1),
            (self.position.x - 1, self.position.y + 2)
        ]
        for x, y in all_positions:
            if x < 0 or x > 7 or y < 0 or y > 7:
                continue
            yield Direction(Position.from_xy(x, y), limit=1)
        pass


class Rook(Figure):
    _price = 5
    _char = 'r'

    def directions(self, attack: bool = False) -> Iterator[Direction]:
        yield Up(self.position)
        yield Down(self.position)
        yield Left(self.position)
        yield Right(self.position)


class Queen(Figure):
    _price = 9
    _char = 'q'

    def directions(self, attack: bool = False) -> Iterator[Direction]:
        yield Up(self.position)
        yield Down(self.position)
        yield Left(self.position)
        yield Right(self.position)
        yield UpLeft(self.position)
        yield UpRight(self.position)
        yield DownLeft(self.position)
        yield DownRight(self.position)


class King(Figure):
    _price = 999
    _char = 'k'

    def initial_pos(self):
        if self.color == Player.WHITE:
            return self.position.index == 4
        return self.position.index == 60

    def directions(self, attack: bool = False) -> Iterator[Direction]:
        rooking = 2 if not attack and self.moves == 0 and self.initial_pos() else 1

        yield Up(self.position, limit=1)
        yield Down(self.position, limit=1)
        yield Left(self.position, limit=rooking)
        yield Right(self.position, limit=rooking)
        yield UpLeft(self.position, limit=1)
        yield UpRight(self.position, limit=1)
        yield DownLeft(self.position, limit=1)
        yield DownRight(self.position, limit=1)

