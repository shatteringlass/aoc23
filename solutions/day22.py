import dataclasses
import enum
from queue import PriorityQueue
from typing import Tuple

from util import read_input


class Axis(enum.Enum):
    X = 0
    Y = 1
    Z = 2


class Brick:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.below = []
        self.above = []
        self.floor = self.min_for_axis(Axis.Z)
        self.height = (self.max_for_axis(Axis.Z) - self.min_for_axis(Axis.Z))

    def min_for_axis(self, axis: Axis) -> int:
        return self._axis_limit(min, axis)

    def max_for_axis(self, axis: Axis) -> int:
        return self._axis_limit(max, axis)

    def _axis_limit(self, func, axis: Axis) -> int:
        return func(self.start[axis.value], self.end[axis.value])

    def __lt__(self, other: "Brick") -> bool:
        return self.floor < other.floor

    def intersects(self, other: "Brick") -> bool:
        (
            (this_area_start_x, this_area_start_y),
            (this_area_end_x, this_area_end_y)
        ) = self.area_xy
        (
            (other_area_start_x, other_area_start_y),
            (other_area_end_x, other_area_end_y)
        ) = other.area_xy

        # check if they are x-adjacent
        if (
            (this_area_end_x < other_area_start_x)
            or (this_area_start_x > other_area_end_x)
        ):
            return False

        # check if they are y-adjacent
        if (
            (this_area_start_y > other_area_end_y)
            or (this_area_end_y < other_area_start_y)
        ):
            return False

        return True

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

    @property
    def is_redundant(self) -> bool:
        if len(self.above) > 0:
            if sum(1 for b in self.above if len(b.below) > 1) == len(self.above):
                return True
        else:
            return True

    @property
    def fall_stack(self):
        return [s for s in self.above if len(s.below) == 1]


def parse_brick(coords):
    points = tuple(tuple(int(c) for c in p.split(","))
                   for p in coords.split("~"))
    return Brick(*points)


def parse_puzzle(puzzle):

    bricks = PriorityQueue()

    min_floor = None

    for brick in puzzle:
        bricks.put(brick)
        if min_floor is None or min_floor > brick.floor:
            min_floor = brick.floor

    return bricks, min_floor


def find_redundant(bricks):
    return list(brick for brick in bricks if brick.is_redundant)


def chain_reaction(bricks: list[Brick]):
    result = list()

    for brick in bricks:
        # get bricks directly on top with no other supporting brick
        fall_stack = brick.fall_stack
        fallen = set()

        while fall_stack:
            falling = fall_stack.pop(0)
            fallen.add(falling)
            for b in falling.above:
                if set(b.below).issubset(fallen):
                    # propagate upwards
                    fall_stack.append(b)
        
        result.extend(fallen)

    return result


def stabilize_bricks(bricks: list[Brick], floor_level: int):
    stable_bricks = []

    while not bricks.empty():
        brick = bricks.get()
        if brick.floor == floor_level:
            stable_bricks.append(brick)
        else:
            below, level = list(), 0

            for sb in stable_bricks:
                if sb.intersects(brick):
                    sb_top = sb.floor + sb.height
                    if sb_top > level:
                        # speed-run to top of tower
                        below, level = list(), sb_top
                    if sb_top == level:
                        # take note of underlying block
                        below.append(sb)

            brick.below = below
            brick.floor = level + 1
            stable_bricks.append(brick)

            for sb in below:
                sb.above.append(brick)

    return stable_bricks


def get_solution(part):

    solution = 0
    puzzle = [parse_brick(coords)
              for coords in read_input('day22').splitlines()]
    bricks, min_floor = parse_puzzle(puzzle)
    bricks = stabilize_bricks(bricks, min_floor)

    if part == 1:
        solution = len(find_redundant(bricks))

    elif part == 2:
        solution = len(chain_reaction(bricks))

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
