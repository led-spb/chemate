import chemate.core
from chemate.core import Position
import chemate.directions


class TestDirections:
    def test_one(self):
        direction = chemate.core.Direction(Position.from_char('e4'), limit=1)
        assert list(map(str, direction)) == ['e4']

        direction = chemate.core.Direction(Position.from_char('a4'), limit=4)
        assert list(map(str, direction)) == ['a4', 'a4', 'a4', 'a4']

    def test_up(self):
        direction = chemate.directions.Up(Position.from_char('a1'))
        assert list(map(str, direction)) == ['a2', 'a3', 'a4', 'a5', 'a6', 'a7', 'a8']

    def test_down(self):
        direction = chemate.directions.Down(Position.from_char('a8'))
        assert list(map(str, direction)) == ['a7', 'a6', 'a5', 'a4', 'a3', 'a2', 'a1']

    def test_left(self):
        direction = chemate.directions.Left(Position.from_char('h8'))
        assert list(map(str, direction)) == ['g8', 'f8', 'e8', 'd8', 'c8', 'b8', 'a8']

    def test_right(self):
        direction = chemate.directions.Right(Position.from_char('a8'))
        assert list(map(str, direction)) == ['b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']

    def test_up_right(self):
        direction = chemate.directions.UpRight(Position.from_char('a1'))
        assert list(map(str, direction)) == ['b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8']

        direction = chemate.directions.UpRight(Position.from_char('a8'))
        assert list(map(str, direction)) == []

        direction = chemate.directions.UpRight(Position.from_char('h2'))
        assert list(map(str, direction)) == []

    def test_up_left(self):
        direction = chemate.directions.UpLeft(Position.from_char('h1'))
        assert list(map(str, direction)) == ['g2', 'f3', 'e4', 'd5', 'c6', 'b7', 'a8']

        direction = chemate.directions.UpLeft(Position.from_char('h8'))
        assert list(map(str, direction)) == []

        direction = chemate.directions.UpLeft(Position.from_char('a1'))
        assert list(map(str, direction)) == []

    def test_down_right(self):
        direction = chemate.directions.DownRight(Position.from_char('a8'))
        assert list(map(str, direction)) == ['b7', 'c6', 'd5', 'e4', 'f3', 'g2', 'h1']

        direction = chemate.directions.DownRight(Position.from_char('h8'))
        assert list(map(str, direction)) == []

        direction = chemate.directions.DownRight(Position.from_char('a1'))
        assert list(map(str, direction)) == []

    def test_down_left(self):
        direction = chemate.directions.DownLeft(Position.from_char('h8'))
        assert list(map(str, direction)) == ['g7', 'f6', 'e5', 'd4', 'c3', 'b2', 'a1']

        direction = chemate.directions.DownLeft(Position.from_char('a8'))
        assert list(map(str, direction)) == []

        direction = chemate.directions.DownLeft(Position.from_char('h1'))
        assert list(map(str, direction)) == []
