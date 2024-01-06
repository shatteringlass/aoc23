import heapq
import dataclasses
import enum

from util import read_input


class Rotation(enum.Enum):
    NULL = ((1, 0), (0, 1))
    CW = ((0, -1), (1, 0))
    CCW = ((0, 1), (-1, 0))


class Direction(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def rotate(self, rot):
        def mult(x): return x[0]*x[1]
        return tuple(
            map(
                sum,
                (
                    tuple(map(mult, zip(self.value, rot.value[0]))),
                    tuple(map(mult, zip(self.value, rot.value[1])))
                )
            )
        )


@dataclasses.dataclass
class State:
    cost: int = 0
    pos: tuple[int, int] = (0, 0)
    drn: Direction = Direction.RIGHT
    cnt: int = 1

    def __lt__(self, other):
        return self.cost < other.cost


class Grid:

    def __init__(self, grid):
        self.grid = {
            (ridx, cidx): int(col)
            for ridx, row in enumerate(grid)
            for cidx, col in enumerate(row)
        }

        self.max_row = len(grid)-1
        self.max_col = len(grid[0])-1

    def get_cost(self, pos):
        return self.grid[pos]

    def is_state_feasible(self, state):
        return state.pos in self.grid

    def step(self, point, drn):
        return tuple(map(sum, zip(point, drn)))

    def move(self, state, rot=Rotation.NULL):
        # print(f"Current state: {state}, selected rotation: {rot}")
        drn = state.drn.rotate(rot)
        pos = self.step(state.pos, drn)
        # print(f"New direction: {Direction(drn)}, New position: {pos}")
        new_state = State(
            cost=state.cost,
            pos=pos,
            drn=Direction(drn),
            cnt=1 if rot != Rotation.NULL else 1+state.cnt,
        )
        # print(f"Moving from {state} to {new_state}")
        return new_state

    def get_valid_states(self, state, min_steps, max_steps):
        # a step is not valid if
        # (1) it ends outside the grid or
        # (2) you reach it by advancing in a straight line for more than max_steps
        # (3) you reach it by turning after advancing in a straight line for less than min_steps
        for rot in (Rotation.NULL, Rotation.CCW, Rotation.CW):
            new_state = self.move(state, rot)
            if self.is_state_feasible(new_state):
                if rot == Rotation.NULL:
                    if state.cnt >= max_steps:
                        # Avoid going straight for too long
                        continue
                else:
                    if state.cnt < min_steps:
                        # Avoid turning too early
                        continue
                yield new_state

    def navigate(self, start, destination, min_steps=0, max_steps=3):

        seen = set()
        queue = [
            State(pos=start, cost=0, drn=Direction.RIGHT),
            State(pos=start, cost=0, drn=Direction.DOWN)
        ]

        while queue:

            state = heapq.heappop(queue)

            if state.pos == destination and state.cnt >= min_steps:
                # print("Reached destination")
                return state.cost

            if (state.pos, state.drn, state.cnt) in seen:
                # there is a loop, ignore this branch
                continue

            seen.add((state.pos, state.drn, state.cnt))

            for new_state in self.get_valid_states(state, min_steps=min_steps, max_steps=max_steps):
                new_state.cost += self.get_cost(new_state.pos)
                # print(f"Updated cost: {new_state.cost}")
                heapq.heappush(queue, new_state)

        # print("Terminating without reaching destination.")
        return -1  # only reached when destination unavailable


def get_solution(part):

    solution = 0
    grid = Grid(read_input('day17').splitlines())
    start = (0, 0)
    dest = (grid.max_row, grid.max_col)

    # print(f"Start: {start} --> Destination: {dest}")

    if part == 1:
        solution = grid.navigate(start, dest, 0, 3)

    elif part == 2:
        solution = grid.navigate(start, dest, min_steps=4, max_steps=10)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
