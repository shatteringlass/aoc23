from util import read_input


def parse_board(board):
    moving, fixed = set(), set()
    for r, row in enumerate(board):
        for c, col in enumerate(row):
            if col == 'O':
                moving.add((r, c))
            elif col == '#':
                fixed.add((r, c))
    return moving, fixed, r+1, c+1


def rotate_90(points, height):
    return set((c, -r + (height - 1)) for (r, c) in points)


def roll_points(points, walls):

    moved = walls.copy()

    for (r, c) in sorted(points, key=lambda x: x[0]):
        r -= 1
        while r >= 0 and (r, c) not in moved:
            r -= 1

        moved.add((r+1, c))

    return moved - walls


def spin(moving, fixed, height, width):
    # keep track of state
    seen = {frozenset(moving): 0}

    cycles = 10**9

    for i in range(cycles):
        for h in (height, width, height, width):
            moving = rotate_90(roll_points(moving, fixed), h)
            fixed = rotate_90(fixed, h)

        key = frozenset(moving)
        if key in seen:
            break

        seen[key] = i+1

    # Once a cycle is found, speed run to the final configuration

    cycle_start = seen[key]
    cycle_len = i - cycle_start + 1
    left = cycles - cycle_start
    final = left % cycle_len + cycle_start

    for k, v in seen.items():
        if v == final:
            break

    return sum(map(lambda point: height - point[0], k))


def print_board(moving, fixed, height, width):
    for r in range(height):
        line = ""
        for c in range(width):
            line += 'O' if (r, c) in moving else '#' if (r,
                                                         c) in fixed else '.'
        print(line)


"""

def roll_row(row):
    # let balls roll to the right

    load = 0
    walls = [idx for idx, ch in enumerate(
        row) if ch == '#']
    new_row = [ch if ch != 'O' else '.' for ch in row]

    balls = 0

    for idx, char in enumerate(row):

        if walls and idx > walls[0]:
            balls = 0
            walls = walls[1:]

        if char == 'O':

            if walls:
                new_pos = walls[0] - balls - 1
            else:
                new_pos = len(row) - 1 - balls

            new_row[new_pos] = 'O'
            load += (new_pos+1)
            balls += 1

    return new_row, load


def transpose_board(board, angle):
    for _ in range(angle//90):
        board = list(zip(*board))

    return board


def roll_board(board, transpose=False, direction='right'):
    #print("See the input board below:")
    # print_board(board)

    if transpose:
        board = transpose_board(board, 90)
        #print("Board transposed, see result below:")
        # print_board(board)

    total_load = 0
    rows = []

    for row in board:
        new_row, load = roll_row(row[::-1 if direction == 'left' else 1])
        total_load += load
        rows.append(new_row)

    #print("Rocks rolled. See result below:")
    # print_board(rows)

    return rows, total_load


cache = {}


def spin(board, iteration=0):

    if board in cache and cache[board] == iteration:
        print("# cycle detected")
        pass

    #print("Rolling north ...")
    board, _ = roll_board(board, transpose=True, direction='left')
    #input("Press a key to continue...")
    #print("Rolling west...")
    board, _ = roll_board(board, transpose=True, direction='left')
    #input("Press a key to continue...")
    #print("Rolling south...")
    board, _ = roll_board(board, transpose=True, direction='right')
    #input("Press a key to continue...")
    #print("Rolling east...")
    board, _ = roll_board(board, transpose=True, direction='right')
    #input("Press a key to continue...")

    cache[board] = iteration

    return board
"""


def get_solution(part):

    solution = 0

    board = read_input('day14').splitlines()

    moving, fixed, height, width = parse_board(board)

    if part == 1:
        solution = sum(map(lambda point: height -
                           point[0], roll_points(moving, fixed)))
        #rolled, _ = roll_board(board, transpose=True, direction='left')
        #solution = check_load(transpose_board(rolled, 90))
    else:
        solution = spin(moving, fixed, height, width)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
