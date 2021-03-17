from abc import abstractmethod
from chemate.figure import Figure, Pawn, Rook, Knight, Bishop, Queen, King
from chemate.utils import Position, Player


class PositionFactory:
    @abstractmethod
    def figures(self):
        """
        :rtype: Iterator of Figure
        """
        pass


class EmptyPosition(PositionFactory):
    def figures(self):
        yield from ()


class InitialPosition(PositionFactory):
    def figures(self):
        yield from self._initial_figures(Player.WHITE)
        yield from self._initial_figures(Player.BLACK)

    def _initial_figures(self, color):
        # Pawns
        for x in range(0, 8, 1):
            yield Pawn(color, Position(x, 1 if color == Player.WHITE else 6))
        # Towers
        for x in range(0, 8, 7):
            yield Rook(color, Position(x, 0 if color == Player.WHITE else 7))
        # Horses
        for x in range(1, 7, 5):
            yield Knight(color, Position(x, 0 if color == Player.WHITE else 7))
        # Elephants
        for x in range(2, 6, 3):
            yield Bishop(color, Position(x, 0 if color == Player.WHITE else 7))
        # Queen
        yield Queen(color, Position(3, 0 if color == Player.WHITE else 7))
        # King
        yield King(color, Position(4, 0 if color == Player.WHITE else 7))
