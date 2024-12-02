# -*- coding: utf-8 -*-
import math
import sys
from datetime import datetime
from itertools import combinations
from timeit import default_timer as timer

import networkx as nx
from colorama import Back, Fore, init
from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

components = set()
components_gravity = {}
connections = set()


def read_file(filename, part=1):
    components.clear()
    connections.clear()
    f = open(filename, "r")
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        first, connected = line.split(":")
        connected = connected.strip().split()
        components.add(first)
        for c in connected:
            components.add(c)
            components_gravity[first] = (
                components_gravity[first] + 1 if first in components_gravity else 1
            )
            components_gravity[c] = (
                components_gravity[c] + 1 if c in components_gravity else 1
            )
            connections.add(tuple(sorted([first, c])))


def create_graph(components, connections):
    g = nx.Graph()
    for c in components:
        g.add_node(c)
    for c in connections:
        g.add_edge(c[0], c[1], capacity=1)
    g = g.to_undirected()
    return g


def solve(part=1, way=1):
    res = 0
    G = create_graph(components, connections)

    if way == 1:
        combinations_of_three = list(
            combinations(connections, 3)
        )  # Generate combinations of three elements
        removed = []
        for combination in combinations_of_three:
            G.remove_edges_from(combination)
            sub_graphs = list(G.subgraph(c) for c in nx.connected_components(G))
            if len(sub_graphs) == 2:
                removed = combination
                res = sub_graphs[0].number_of_nodes() * sub_graphs[1].number_of_nodes()
                break
            G.add_edges_from(combination)
        print_color(
            f"---------> removed: {removed} <---------",
            Fore.LIGHTRED_EX,
            Back.LIGHTYELLOW_EX,
        )
    else:
        for node1, node2 in combinations(G.nodes, 2):
            cuts, partitions = nx.minimum_cut(G, node1, node2)
            if cuts == 3:
                break
        res = math.prod(map(len, partitions))

    print_color(
        f"---------> final result: {res} <---------",
        Fore.LIGHTRED_EX,
        Back.LIGHTYELLOW_EX,
    )
    return res


def puzzle1(filename, way=1):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part=1, way=way)
    t_end = timer()
    print_color(f"Time elapsed (in seconds): {t_end - t_start}", Fore.MAGENTA)
    return res


def puzzle2(filename):
    t_start = timer()
    print_color(f"puzzle2: {filename}", Fore.MAGENTA)
    read_file(filename, part=2)
    res = solve(part=2)
    t_end = timer()
    print(f"Time elapsed (in seconds): {t_end - t_start}")
    return res


if __name__ == "__main__":
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    # assert puzzle1('../../puzzles/2023/25/example.txt', way=1) == 54
    # assert puzzle1('../../puzzles/2023/25/example.txt', way=2) == 54
    # assert puzzle1('../../puzzles/2023/25/input.txt', way=1) == -1 # way 1, brute force won't run
    # assert puzzle1('../../puzzles/2023/25/input.txt', way=2) == 555702

    assert puzzle2("../../puzzles/2023/25/example.txt") == -1
    # assert puzzle2('../../puzzles/2023/25/input.txt') == -1  # won't run

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
