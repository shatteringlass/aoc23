import dataclasses
from util import read_input
from random import choice
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


def contract_edges(vertices, edges):
    vert_groups = {v: set([v]) for v in vertices}

    while len(vert_groups.keys()) > 2:
        try:
            src, dst = choice(edges)
        except IndexError:
            print(edges)
            raise
        vert_groups[src] = vert_groups[src].union(vert_groups[dst])
        vert_groups.pop(dst, None)

        new_edges = list()

        for s, d in edges:
            if s == dst:
                if d == src:
                    continue
                e = (src, d)
            elif d == dst:
                if s == src:
                    continue
                e = (s, src)
            else:
                e = (s, d)
            new_edges.append(e)

        edges = new_edges

    return vert_groups, edges


def find_cut(vertices, edges):

    while True:
        vert_groups, edges = contract_edges(vertices.copy(), edges.copy())

        if all(len(v) > 1 for v in vert_groups.values()) and len(edges) == 3:
            size = 1
            for vg in vert_groups.values():
                size *= len(vg)
            return size


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
