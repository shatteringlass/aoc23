"""

The input consists of many records in the form of:

SPRINGS, GROUPS

Where SPRINGS is a string constitued by the following symbols:

. operational
# damaged
? unknown

And GROUPS is a comma-separated list of integers repsententing the 
length of continous intervals groups of damaged springs.

For each row, count all of the different arrangements of
operational and broken springs that meet the given criteria.
What is the sum of those counts?

"""

from functools import cache
from util import read_input

i = read_input('day12').split('\n')


@cache
def solve(springs, groups, curlen=0):
    if not springs:
        # no more springs left
        if (not groups and curlen == 0):
            # no more groups left and no hanging group
            return 1
        elif (len(groups) == 1 and groups[0] == curlen):
            # one group left with the same size as the current group
            return 1
        else:
            return 0
    else:
        # more springs left
        if (groups and curlen > groups[0]):
            # building an oversized group
            return 0
        elif (not groups and curlen):
            # building an unnecessary group
            return 0
        else:
            # current group is shorter than target, keep growing
            char, springs = springs[0], springs[1:]
            total = 0

            if char in '#?':
                # assume the group grows and explore the subproblem
                total += solve(springs, groups, curlen + 1)

            if char in '.?':
                if not curlen:
                    # no ongoing group, explore the subproblem
                    total += solve(springs, groups, 0)
                elif curlen == groups[0]:
                    # assume the group ends successfully and explore the subproblem
                    total += solve(springs, groups[1:], 0)

            return total


def get_solution(part):

    total = 0

    for line in i:
        records, groups = line.split()
        groups = tuple(map(int, groups.split(',')))

        if part == 1:
            total += solve(records, groups)
            solve.cache_clear()

        if part == 2:
            total += solve('?'.join([records] * 5), groups * 5)
            solve.cache_clear()

    return total


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
