import re

from util import read_input

i = read_input('day1')


numre = re.compile(r'\d')
numbers = [
    ('one', 'o1e'), ('two', 't2o'),
    ('three', 't3e'), ('four', 'f4r'),
    ('five', 'f5e'), ('six', 's6x'),
    ('seven', 's7n'), ('eight', 'e8t'),
    ('nine', 'n9e')
]

digre = {re.compile(n[0]): n[1] for n in numbers}


def compute_solution(part):
    result = 0

    for line in i.split('\n'):

        if part == 2:
            for k, v in digre.items():
                line = re.sub(k, v, line)

        digits = re.findall(numre, line)

        if digits:
            value = int(digits[0])*10 + int(digits[-1])
            result += value

    return result


print(f"Solution for part 1 is: {compute_solution(1)}")
print(f"Solution for part 2 is: {compute_solution(2)}")
