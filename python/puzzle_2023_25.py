import sys
from datetime import datetime
from itertools import combinations
from timeit import default_timer as timer

import networkx as nx
from colorama import Fore, Back, init

from utils.utils import print_color

print(sys.getrecursionlimit())
sys.setrecursionlimit(10000)

components = set()
connections = set()


def read_file(filename, part=1):
    components.clear()
    connections.clear()
    f = open(filename, "r")
    for i, line in enumerate(f):
        line = line.strip()
        if line == "":
            continue
        first, connected = line.split(':')
        connected = connected.strip().split()
        components.add(first)
        for c in connected:
            components.add(c)
            connections.add(tuple(sorted([first, c])))


def create_graph(components, connections):
    g = nx.Graph()
    for c in components:
        g.add_node(c)
    for c in connections:
        g.add_edge(c[0], c[1])
    g = g.to_undirected()
    return g


def solve(part=1):
    res = 0
    g = create_graph(components, connections)
    combinations_of_three = list(combinations(connections, 3))  # Generate combinations of three elements

    removed = []
    for combination in combinations_of_three:
        for connection in combination:
            g.remove_edge(connection[0], connection[1])
        sub_graphs = list(g.subgraph(c) for c in nx.connected_components(g))
        if len(sub_graphs) == 2:
            removed = combination
            res = sub_graphs[0].number_of_nodes() * sub_graphs[1].number_of_nodes()
            break
        for connection in combination:
            g.add_edge(connection[0], connection[1])

    print_color(f"---------> removed: {removed} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    print_color(f"---------> final result: {res} <---------", Fore.LIGHTRED_EX, Back.LIGHTYELLOW_EX)
    return res


def puzzle1(filename):
    t_start = timer()
    print_color(f"puzzle1: {filename}", Fore.MAGENTA)
    read_file(filename)
    res = solve(part=1)
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    init()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"Start Time = {current_time}", Fore.YELLOW)

    assert puzzle1('../puzzles/2023/25/example.txt') == 54
    assert puzzle1('../puzzles/2023/25/input.txt') == -1
    # assert puzzle2('../puzzles/2023/25/example.txt') == -1
    # assert puzzle2('../puzzles/2023/25/input.txt') == -1  # won't run

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print_color(f"End Time = {current_time}", Fore.YELLOW)
