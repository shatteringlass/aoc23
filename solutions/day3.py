import math
import re

from util import read_input

i = read_input('day3').split('\n')

"""
Question 1:
Any number adjacent to a symbol, even diagonally, 
is a "part number" and should be included in your sum. 
Periods (.) do not count as a symbol.
What is the sum of all of the part numbers in the engine schematic?

Question 2:
A gear is any * symbol that is adjacent to exactly two part numbers. 
Its gear ratio is the result of multiplying those two numbers together.
What is the sum of all of the gear ratios in your engine schematic?
"""

totrows = len(i)
totcols = len(i[0])


def grab_numbers(string):
    numpat = re.compile(r'\d+')
    return [(m.group(), m.start(0), m.end(0)) for m in re.finditer(numpat, string)]


def grab_candidate_gears(string):
    gearpat = re.compile(r'\*')
    return [m.start(0) for m in re.finditer(gearpat, string)]


def check_gear(x, y):
    # find numbers adjacent to x,y and return their product
    numbers = []

    startrow = max(0, y-1)
    endrow = min(totrows, y+1)

    for line in i[startrow:endrow+1]:
        neighbors = grab_numbers(line)
        print(neighbors)
        for (num, xs, xe) in neighbors:
            if x > xe or x < xs-1:
                continue
            else:
                numbers.append(int(num))
                print(f"Found {num} on line {y} starting at {xs} ending at {xe}")

    if len(numbers) != 0 and len(numbers) != 2:
        return 0

    return math.prod(numbers)


def check_neighbors(x_start, x_end, y):
    sympat = re.compile(r'[^0-9\.]')
    check = False
    startrow = max(0, y-1)
    endrow = min(totrows, y+1)
    startcol = max(0, x_start-1)
    endcol = min(x_end+1, totcols)
    for x in i[startrow:endrow+1]:
        haystack = x[startcol:endcol]
        has_symbols = bool(re.search(sympat, haystack))
        check = check or has_symbols
    return check


def compute_solution(part):
    result = 0

    if part == 1:
        for y, line in enumerate(i):
            print(f"Currently at line {y}")
            for (num, xs, xe) in grab_numbers(line):
                if check_neighbors(xs, xe, y):
                    print(f"Number {num} has symbol neighbors.")
                    result += int(num)
                else:
                    print(f"Number {num} does not have symbol neighbors.")

    elif part == 2:
        for y, line in enumerate(i):
            for x in grab_candidate_gears(line):
                result += check_gear(x, y)

    return result


print(f"Solution for part 1 is: {compute_solution(1)}")
print(f"Solution for part 2 is: {compute_solution(2)}")
