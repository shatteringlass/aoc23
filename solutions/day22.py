from util import read_input
import dataclasses
from typing import Tuple
import enum


class Axis(enum.Enum):
    X = 0
    Y = 1
    Z = 2


@dataclasses.dataclass(frozen=True)
class Brick:
    start: Tuple[int, int, int]
    end: Tuple[int, int, int]
    above: set[Brick]
    below: set[Brick]

    def is_removable(self, bricks):
        for brick in self.above:
            if len(bricks[brick].below) == 1:
                return False

        return True

    def min_for_axis(self, axis: Axis) -> int:
        return self._axis_limit(min, axis)

    def max_for_axis(self, axis: Axis) -> int:
        return self._axis_limit(max, axis)

    def _axis_limit(self, func, axis: Axis) -> int:
        return func(self.start[axis.value], self.end[axis.value])

    def __lt__(self, other: "Brick") -> bool:
        return self.min_for_axis(Axis.Z) < other.min_for_axis(Axis.Z)

    def update_z(self, new_z: int) -> "Brick":
        delta = (0, 0, self.min_for_axis(Axis.Z) - new_z)
        return Brick(*(tuple(map(sum, zip(coord, delta))) for coord in (self.start, self.end)))

    @property
    def height(self) -> int:
        return (self.max_for_axis(Axis.Z) - self.min_for_axis(Axis.Z) + 1)

    @property
    def area_xy(self) -> tuple[tuple[int, int]]:
        return (
            (
                self.min_for_axis(Axis.X),
                self.min_for_axis(Axis.Y)
            ),
            (
                self.max_for_axis(Axis.X),
                self.max_for_axis(Axis.Y)
            )
        )

    def intersects(self, other: "Brick") -> bool:
        (
            (this_area_start_x, this_area_start_y),
            (this_area_end_x, this_area_end_y)
        ) = self.area_xy()
        (
            (other_area_start_x, other_area_start_y),
            (other_area_end_x, other_area_end_y)
        ) = other.area_xy()

        # check if they are next to one another
        if this_area_end_x < other_area_start_x or this_area_start_x > other_area_end_x:
            return False

        # check if they are on top of one another
        if this_area_start_y > other_area_end_y or this_area_end_y < other_area_start_y:
            return False

        return True


def parse_brick(coords):
    points = ((int(c) for c in p.split(",")) for p in coords.split("~"))
    return Brick(*points)


def build_graph(bricks):
    graph = dict()
    for brick in bricks:
        pass


def drop_once(bricks):

    supports = dict()
    supported_by = dict()

    min_x, min_y, max_x, max_y = 0, 0, 0, 0

    for brick in bricks:
        min_x = min(brick.min_for_axis(Axis.X), min_x)
        min_y = min(brick.min_for_axis(Axis.Y), min_y)
        max_x = max(brick.max_for_axis(Axis.X), max_x)
        max_y = max(brick.max_for_axis(Axis.Y), max_y)

    heights = [
        [0 for y in range(max_y-min_y+1)]
        for x in range(max_x-min_x+1)
    ]

    for brick in bricks:
        area_start, area_end = brick.area_xy()
        old_max_height = max(
            row[area_start[1]:area_end[1]+1]
            for row in heights[area_start[0]:area_end[0]+1]
        )
        brick.update_z(old_max_height + 1)
        new_max_height = old_max_height + brick.height
        heights

    return bricks


def drop_to_floor(bricks):
    while len(drop_once(bricks) > 0):
        pass

    return bricks


def get_solution(part):

    solution = 0

    bricks = sorted([parse_brick(coords)
                    for coords in read_input('day22').splitlines()])

    if part == 1:
        # count bricks that are either
        # - not supporting any other brick or
        # - supporting another brick that is also supported by a second brick
        drop_to_floor(bricks)

    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
