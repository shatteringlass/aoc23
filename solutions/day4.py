import math
import re

from util import read_input

i = read_input('day4').split('\n')

"""
Question 1:
you have to figure out which of the numbers 
you have appear in the list of winning numbers. 
The first match makes the card worth one point 
and each match after the first doubles the point 
value of that card.
How many points are they worth in total?

Question 2:
There's no such thing as "points". 
Instead, scratchcards only cause you to win 
more scratchcards equal to the number of winning numbers you have.

Specifically, you win copies of the scratchcards below the winning card 
equal to the number of matches. 
So, if card 10 were to have 5 matching numbers, 
you would win one copy each of cards 11, 12, 13, 14, and 15.

Copies of scratchcards are scored like normal scratchcards 
and have the same card number as the card they copied. 
So, if you win a copy of card 10 and it has 5 matching numbers, 
it would then win a copy of the same cards that the original card 10 won: 
cards 11, 12, 13, 14, and 15. 
This process repeats until none of the copies cause you to win any more cards. 
(Cards will never make you copy a card past the end of the table.)

Process all of the original and copied scratchcards until no more scratchcards are won. 
Including the original set of scratchcards, how many total scratchcards do you end up with?
"""


def parse_input():
    matches = []
    for line in i:
        card, numbers = line.split(": ")
        winning, own = numbers.split(" | ")
        winning = [int(x) for x in winning.split()]
        own = [int(x) for x in own.split()]
        matches.append(len([x for x in own if x in winning]))
    return matches


def compute_solution(part):
    result = 0

    matches = parse_input()

    if part == 1:
        for match in matches:
            score = 2**(match-1) if match else 0
            result += score
    elif part == 2:

        cards = {k: 1 for k in range(len(matches))}

        for idx, match in enumerate(matches):
            for x in range(1, match+1):
                # convert each card into its x-degree neighbour
                cards[idx+x] += cards[idx]

        result = sum(cards.values())

    return result


print(f"Solution for part 1 is: {compute_solution(1)}")
print(f"Solution for part 2 is: {compute_solution(2)}")
