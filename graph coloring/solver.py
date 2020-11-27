from copy import deepcopy
from random import shuffle


def constrain(i, adj, coloring, c):
    for j in adj[i]:
        if not type(coloring[j]) is int and c in coloring[j]:
            coloring[j].remove(c)
    return coloring


calls = 0


def backtrack(nodes, adj, coloring, uncolored):
    global calls

    if calls == 5_000_000:
        return False, None

    calls += 1

    if len(uncolored) == 0:
        return True, coloring

    (_, _, uncolored_node, index) = min((len(coloring[uncolored_node]), len(adj[uncolored_node]), uncolored_node, index) for (index, uncolored_node) in enumerate(uncolored))

    domain = coloring[uncolored_node].copy()
    #shuffle(domain)
    for c in domain:
        coloring[uncolored_node] = c
        next_success, solution = backtrack(nodes, adj, constrain(uncolored_node, adj, deepcopy(coloring), c), uncolored[:index] + uncolored[index + 1:])
        if next_success:
            return True, solution
        coloring[uncolored_node] = domain
    return False, None


def greedy(number_nodes, adj):
    nodes = sorted(list(range(number_nodes)), key=lambda node: len(adj[node]), reverse=True)
    color_map = list(-1 for _ in range(number_nodes))

    for node in nodes:
        available_colors = set(range(number_nodes))
        for neighbor in adj[node]:
            if color_map[neighbor] > -1:
                neigh_color = color_map[neighbor]
                if neigh_color in available_colors:
                    available_colors.remove(neigh_color)
        color_map[node] = min(available_colors)

    return color_map


def solve_it(input_data):
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    adj = [[] for _ in range(node_count)]
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        u, v = int(parts[0]), int(parts[1])
        adj[u].append(v)
        adj[v].append(u)

    '''
    global calls
    for max_color in range(5, 15):
        print("----" + str(max_color) + " colors----")
        coloring, uncolored = [list(range(max_color)) for _ in range(node_count)], list(range(node_count))
        success, solution = backtrack(node_count, adj, coloring, uncolored)

        print(str(calls) + " calls")
        calls = 0

        if success:
            return solution
    '''

    solution = greedy(node_count, adj)

    coloring_str = ""
    num_colors = 0
    for c in solution:
        coloring_str += str(c) + " "
        num_colors = max(num_colors, c)

    return str(num_colors + 1) + " 0\n" + coloring_str


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        #print("Solving: " + file_location)
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        #with open("sol.txt", 'w') as f:
            #f.write(solve_it(input_data))

        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
