"""
In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand.
A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect.
Start by comparing the first card in each hand.
If these cards are different, the hand with the stronger first card is considered stronger.
If the first card in each hand have the same label, however, then move on to considering the second card in each hand.
If they differ, the hand with the higher second card wins;
otherwise, continue with the third card in each hand, then the fourth, then the fifth.

Find the rank of every hand in your set. What are the total winnings?

"""

from util import read_input

i = read_input('day7').split('\n')


class Card:
    def __init__(self, symbol):
        self.ranking = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.symbol = symbol

    @property
    def value(self):
        return self.ranking.index(self.symbol)

    def __str__(self):
        return f"{self.symbol}"


class Hand:
    def __init__(self, cards, bid):
        self.cards = [Card(c) for c in cards]
        self.bid = bid
        self.scores = {'hi': 1, '1p': 2, '2p': 3,
                       '3ok': 4, 'fh': 5, '4ok': 6, '5ok': 7}

    def __eq__(self, y):
        if isinstance(y, Hand):
            return self.strength == y.strength
        raise TypeError

    def __ne__(self, y):
        return not self == y

    def __gt__(self, y):
        if isinstance(y, Hand):
            return self.strength > y.strength
        raise TypeError

    def __lt__(self, y):
        return self != y and not self > y

    def __ge__(self, y):
        return self == y or self > y

    def __le__(self, y):
        return self == y or self < y

    def __str__(self):
        return f"Cards: {''.join([str(c) for c in self.cards])} | Strength: {self.strength} | Bid: {self.bid}"

    @property
    def value(self):
        cnt = {}
        score = 'hi'

        for card in self.cards:
            if card.symbol not in cnt:
                cnt[card.symbol] = 0
            cnt[card.symbol] += 1

        for k, v in cnt.items():
            if v == 2:
                score = '2p' if score == '1p' else 'fh' if score == '3ok' else '1p'
            if v == 3:
                score = 'fh' if score == '1p' else '3ok'
            if v == 4:
                score = '4ok'
            if v == 5:
                score = '5ok'

        return self.scores[score]

    @property
    def strength(self):
        return (self.value, ''.join([f"{c.value:02}" for c in self.cards]))


class Game:
    def __init__(self, entries):
        self.hands = []
        self._sorted = False
        for e in entries:
            cards, bid = e.split()
            self.hands.append(Hand(cards, int(bid)))

    def rank_hands(self):
        if not self._sorted:
            self.hands.sort()
            self._sorted = True

    @property
    def value(self):
        # add up the result of multiplying each hand's bid with its rank
        self.rank_hands()
        return sum([(r+1)*h.bid for (r,h) in enumerate(self.hands)])


def compute_solution(part):
    g = Game(i)
    value = g.value
    for h in g.hands:
        print(str(h))
    return value


print(f"Solution for part 1 is: {compute_solution(1)}")
