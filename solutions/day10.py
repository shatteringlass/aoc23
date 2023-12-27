
"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.

Find the single giant loop starting at S. 
How many steps along the loop does it take to get 
from the starting position to the point farthest 
from the starting position?

IDEA: navigate from both ends and stop when pointers meet

"""
from util import read_input

i = read_input('day10').split('\n')
maxrows = len(i)
maxcols = len(i[0])


def check_boundaries(row, col):
    return row*col > 0 and row < maxrows and col < maxcols


def check_cell(row, col):
    """
    Return the entrance and exit directions for a cell 
    at coordinates row,col having type sym as a list of points
    """
    sym = i[row][col]

    dirs = dict(up=(row-1, col), down=(row+1, col),
                left=(row, col-1), right=(row, col+1))

    if sym == '|':
        directions = [dirs['up'], dirs['down']]
    if sym == '-':
        directions = [dirs['left'], dirs['right']]
    if sym == 'L':
        directions = [dirs['up'], dirs['right']]
    if sym == 'J':
        directions = [dirs['left'], dirs['up']]
    if sym == '7':
        directions = [dirs['left'], dirs['down']]
    if sym == 'F':
        directions = [dirs['down'], dirs['right']]
    if sym == '.':
        directions = []
    if sym == 'S':
        directions = [dirs['up'], dirs['down'],
                      dirs['left'], dirs['right']]

    # print(f"Possible directions for cell at {row,col} with symbol {sym}: {directions}")
    return directions


def find_start(maze):
    for idx, row in enumerate(maze):
        try:
            return idx, row.index('S')
        except ValueError:
            continue


def find_next(curr, prev):
    """
    Return the next step knowing the previous
    """
    # print(f"Checking next cell for {curr} coming from {prev}")
    options = check_cell(*curr)
    return [opt for opt in options if check_boundaries(*opt) and curr in check_cell(*opt) and opt != prev]


def solve(part):

    start = find_start(i)

    o = find_next(start, None)
    p = [start for _ in range(2)]

    loop = [[start, o[0]], [start, o[1]]]

    steps = 1

    while o[0] != o[1]:
        for idx in range(2):
            n = find_next(o[idx], p[idx])
            p[idx] = o[idx]
            o[idx] = n[0]
            loop[idx].append(n[0])
        steps += 1

    loop = sorted(loop[0][:-1] + loop[1][::-1])

    if part == 1:
        return steps

    if part == 2:
        count = 0
        inside = False
        for row, r in enumerate(i):
            for col, _ in enumerate(r):
                if (row, col) not in loop:
                    if inside:
                        count += 1
                    else:
                        continue
                else:
                    if i[row][col] in '|F7':
                        inside = not(inside)

        return count


print(f"Solution for part 1 is: {solve(1)}")
print(f"Solution for part 2 is: {solve(2)}")
