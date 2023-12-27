from util import read_input

i = read_input('day2')

"""
Question 1:
The Elf would first like to know 
which games would have been possible 
if the bag contained only 
12 red cubes, 13 green cubes, and 14 blue cubes?
What is the sum of the IDs of those games?

Question 2:
For each game, find the minimum set of cubes that must have been present. 
What is the sum of the power of these sets?
"""


max_red = 12
max_green = 13
max_blue = 14


def parse_game(game):
    gid, subsets = game.split(':')
    return gid.split()[-1], subsets.split(';')


def parse_subset(subset):
    values = dict(r=0, g=0, b=0)
    for color in subset.split(','):
        if 'blue' in color:
            values['b'] = int(color.split()[0])
        elif 'red' in color:
            values['r'] = int(color.split()[0])
        elif 'green' in color:
            values['g'] = int(color.split()[0])
    return values


def check_subset(subset):
    return subset['r'] <= max_red and subset['g'] <= max_green and subset['b'] <= max_blue


def assess_game(subsets):
    r, g, b = 0, 0, 0
    for subset in subsets:
        ps = parse_subset(subset)
        r = max(r, ps['r'])
        g = max(g, ps['g'])
        b = max(b, ps['b'])
    return r*g*b


def check_game(subsets):
    for subset in subsets:
        if not check_subset(parse_subset(subset)):
            return False
    return True


def compute_solution(part):
    result = 0

    for line in i.split('\n'):
        gid, subsets = parse_game(line)
        if part == 1 and check_game(subsets):
            result += int(gid)
        elif part == 2:
            result += assess_game(subsets)

    return result


print(f"Solution for part 1 is: {compute_solution(1)}")
print(f"Solution for part 2 is: {compute_solution(2)}")
