from .core import Direction


class Up(Direction):
    delta = 8

    def stop_iterate(self) -> bool:
        return self.position.y == 7 or self.limit == 0


class Down(Direction):
    delta = -8

    def stop_iterate(self) -> bool:
        return self.position.y == 0 or self.limit == 0


class Left(Direction):
    delta = -1

    def stop_iterate(self) -> bool:
        return self.position.x == 0 or self.limit == 0


class Right(Direction):
    delta = 1

    def stop_iterate(self) -> bool:
        return self.position.x == 7 or self.limit == 0


class UpLeft(Direction):
    delta = 7

    def stop_iterate(self) -> bool:
        return self.position.y == 7 or self.position.x == 0 or self.limit == 0


class UpRight(Direction):
    delta = 9

    def stop_iterate(self) -> bool:
        return self.position.y == 7 or self.position.x == 7 or self.limit == 0


class DownLeft(Direction):
    delta = -9

    def stop_iterate(self) -> bool:
        return self.position.x == 0 or self.position.y == 0 or self.limit == 0


class DownRight(Direction):
    delta = -7

    def stop_iterate(self) -> bool:
        return self.position.x == 7 or self.position.y == 0 or self.limit == 0
