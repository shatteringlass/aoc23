"""
Starting at AAA, follow the left/right instructions. How many steps are required to reach ZZZ?
"""

from util import read_input

import re

from itertools import cycle
from math import lcm

i = read_input('day8').split('\n')


class Node:

    def __init__(self, desc):
        label, neighbours = desc.split(' = ')
        self.label = label
        left, right = neighbours.split()
        self.left = left[1:4]
        self.right = right[:3]

    @property
    def is_endnode(self):
        return self.label.endswith('Z')

    def __eq__(self, other):
        return self.label == other.label and self.left == other.left and self.right == other.right

    def __neq__(self, other):
        return not(self == other)

    def __str__(self):
        return f"Node(label={self.label}, left={self.left}, right={self.right})"


def find_node(label, nodes):
    pattern = re.compile(f"^{label} =.*$", re.MULTILINE)
    match = pattern.search(nodes)
    return Node(match[0])


def find_ghost_start_nodes(nodes):
    pattern = re.compile(f"^\w+A =.*$", re.MULTILINE)
    match = pattern.findall(nodes)
    return [Node(i) for i in match]


def find_ghost_end_nodes(nodes):
    pattern = re.compile(f"^\w+Z =.*$", re.MULTILINE)
    match = pattern.findall(nodes)
    return [Node(i) for i in match]


def travel(instructions, nodes, current):
    for idx, inst in enumerate(cycle(instructions)):
        if current.is_endnode:
            return idx
        if inst == 'L':
            current = find_node(current.left, nodes)
        else:
            current = find_node(current.right, nodes)


def compute_solution(part):
    instructions = i[0]
    nodes = '\n'.join(i[2:])

    result = 0

    if part == 1:

        current = 'AAA'
        destination = 'ZZZ'

        while current != destination:
            node = find_node(current, nodes)
            if instructions[result % len(instructions)] == 'L':
                current = node.left
            else:
                current = node.right
            result += 1

    if part == 2:
        current = find_ghost_start_nodes(nodes)
        result = lcm(*[travel(instructions, nodes, c) for c in current])

    return result


print(f"Solution for part 1 is: {compute_solution(1)}")
print(f"Solution for part 2 is: {compute_solution(2)}")
