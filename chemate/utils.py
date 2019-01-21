
class Position(object):
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def copy(self):
        return Position(self.x, self.y)

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __str__(self):
        return "%s%d" % (chr(ord('A') + self.x), self.y+1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Direction(object):
    up = Position(x=0, y=1)
    down = Position(x=0, y=-1)
    left = Position(x=-1, y=0)
    right = Position(x=1, y=0)

    up_left = Position(x=-1, y=1)
    up_right = Position(x=1, y=1)
    down_left = Position(x=-1, y=-1)
    down_right = Position(x=1, y=-1)
