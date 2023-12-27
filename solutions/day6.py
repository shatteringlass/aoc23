"""
Question 1:
As part of signing up, you get a sheet of paper (your puzzle input) 
that lists the time allowed for each race and also the best distance 
ever recorded in that race. 
To guarantee you win the grand prize, you need to make sure you go 
farther in each race than the current record holder.

The organizer brings you over to the area where the boat races are held. 
The boats are much smaller than you expected - they're actually toy boats, 
each with a big button on top. 
Holding down the button charges the boat, and releasing the button allows 
the boat to move. Boats move faster if their button was held longer, but 
time spent holding the button counts against the total race time. 
You can only hold the button at the start of the race, 
and boats don't move until the button is released.

To see how much margin of error you have, determine the number of ways 
you can beat the record in each race; in this example, if you 
multiply these values together, you get 288 (4 * 8 * 9).

Determine the number of ways you could beat the record in each race. 
What do you get if you multiply these numbers together?


Question 2:


"""

from util import read_input

import sys

i = read_input('day6').split('\n')


def compute_solution(part):

    if part == 1:
        times = map(lambda x: int(x), i[0].split(':')[1].split())
        distances = map(lambda x: int(x), i[1].split(':')[1].split())
        races = list(zip(times, distances))
    if part == 2:
        times = int(i[0].split(':')[1].replace(" ", ""))
        distances = int(i[1].split(':')[1].replace(" ", ""))
        races = [(times, distances)]
        x1 = (times - (times**2 - 4*distances)**(1/2))*(1/2)
        x2 = (times + (times**2 - 4*distances)**(1/2))*(1/2)
        return int(x2) - int(x1)

    result = 1

    for race in races:
        best_dist = race[1]
        max_time = race[0]
        wins = 0
        at = 1
        while at < max_time:
            time = max_time - at
            dist = at * time
            if dist > best_dist:
                wins += 1
            at += 1
        result *= wins

    return result


print(f"Solution for part 1 is: {compute_solution(1)}")
print(f"Solution for part 2 is: {compute_solution(2)}")
