import heapq
import dataclasses
import enum

from util import read_input

grid = read_input('day17').splitlines()


class Direction(enum.Enum):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


@dataclasses.dataclass
class State:
    cost: int = 0    
    pos: tuple[int, int] = (0, 0)
    drn: Direction = Direction.RIGHT
    cnt: int = 0
    max_row: int = 0
    max_col: int = 0

    @property
    def admissible(self):
        return (self.pos[0] >= 0
                and self.pos[1] >= 0
                and self.pos[0] < max_row
                and self.pos[1] < max_col)

    def turn_cw(self):
        raise NotImplementedError

    def turn_ccw(self):
        raise NotImplementedError


def navigate(grid, destination):

    max_row = len(grid)
    max_col = len(grid[0])

    seen = set()
    queue = [State(drn=Direction.RIGHT, max_row=max_row, max_col=max_col),
             State(drn=Direction.DOWN, max_row=max_row, max_col=max_col)]

    while queue:

        state = heapq.heappop(queue)

        if state.pos == destination:
            return state.cost

        if (state.pos, state.cost) not in seen and state.admissible:
            heapq.heappush(queue, state.turn_cw())
            heapq.heappush(queue, state.turn_ccw())

    return -1  # only reached when destination unavailable


def get_solution(part):

    solution = 0

    if part == 1:
        solution = navigate(grid, (0, 0))

    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
