
from util import read_input
from random import choice
import copy

"""
Find the three wires you need to disconnect in order 
to divide the components into two separate groups. 
What do you get if you multiply the sizes of these two groups together?
"""


def parse_instructions(instr):
    vertices = set()
    edges = list()

    for connection in instr:
        src, dests = connection.split(": ")
        vertices.add(src)
        for dest in dests.split():
            vertices.add(dest)
            edges.append((src, dest))

    return vertices, edges


def contract_edge(src, dst, edges):
    new_edges = list()

    for s, d in edges:
        if ((s, d) == (src, dst)) or ((s, d) == (dst, src)):
            continue
        e = (src if s == dst else s, src if d == dst else d)
        new_edges.append(e)

    return new_edges


def contract_edges(vertices, edges):
    cuts = {v: set([v]) for v in vertices}

    while len(cuts.keys()) > 2:
        src, dst = choice(edges)
        cuts[src] = cuts[src].union(cuts[dst])
        cuts.pop(dst, None)
        edges = contract_edge(src, dst, edges)

    return cuts, edges


def find_cut(vertices, edges):

    cuts = copy.deepcopy(vertices)
    edges = copy.deepcopy(edges)

    while True:
        c, e = contract_edges(cuts, edges)
        if all(len(v) > 1 for v in c.values()) and len(e) == 3:
            vg1, vg2 = c.values()
            return len(vg1)*len(vg2)


def get_solution(part):

    solution = 0
    connections = read_input('day25').splitlines()
    vertices, edges = parse_instructions(connections)

    if part == 1:
        solution = find_cut(vertices, edges)
    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
