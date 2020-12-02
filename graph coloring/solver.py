import os
from random import shuffle
from stopwatch import Stopwatch


def greedy(node_count, nodes, adj):
    """
    With a certain ordering of the nodes, perform the greedy coloring algorithm
    """

    color_map = list(-1 for _ in range(node_count))

    for node in nodes:
        neigh_colors = set(color_map[neighbor] for neighbor in adj[node])

        for color in range(node_count):
            if color not in neigh_colors:
                color_map[node] = color
                break

    return color_map


def permute_nodes(node_count, prev_solution, adj):
    """
    Given a solution, group nodes by colors, then within these groups sort by descending degree
    Shuffle these groups and concatenate, then do the greedy solution on this new node ordering
    This process is guaranteed to produce no worse of a solution than the one it is given
    """

    nodes_lists = []
    for color in range(node_count):
        curr_color = list(node for node in range(node_count) if prev_solution[node] == color)
        if len(curr_color) == 0:
            break
        curr_color.sort(key=lambda node: len(adj[node]), reverse=True)
        nodes_lists.append(curr_color)

    shuffle(nodes_lists)

    nodes = []
    for node_list in nodes_lists:
        nodes.extend(node_list)

    return nodes


def solve_it(input_data, prev_sol=None):
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

    # start with blank solution which is sorted by the first permutation
    solution = list(0 for _ in range(node_count))

    # load in previous solution if file location given
    if prev_sol:
        solution = prev_sol

    stopwatch_greedy = Stopwatch()
    stopwatch_greedy.stop()
    stopwatch_permute = Stopwatch()
    stopwatch_permute.stop()

    iterations = 20000
    for i in range(1, iterations + 1):
        if i % 10 == 0:
            with open("progress.txt", 'w') as f:
                f.write(str(i) + " iterations, " + str(max(solution) + 1) + " colors")

        stopwatch_permute.start()
        nodes = permute_nodes(node_count, solution, adj)
        stopwatch_permute.stop()

        stopwatch_greedy.start()
        solution = greedy(node_count, nodes, adj)
        stopwatch_greedy.stop()

    print("greedy running time: " + str(stopwatch_greedy))
    print("permute running time: " + str(stopwatch_permute))

    return stringify(solution)


def stringify(solution):
    coloring_str = ""
    for color in solution:
        coloring_str += str(color) + " "
    return str(max(solution) + 1) + " 0\n" + coloring_str


def read_sol(file_location):
    if not os.path.exists(file_location):
        return None

    with open(file_location, "r") as f:
        f.readline()
        return list(int(s) for s in f.readline().split(" ") if len(s) > 0)


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

        print_to_file = True

        stopwatch = Stopwatch()
        if print_to_file:
            print("Solving: " + file_location)

            prev_sol = read_sol("solutions/" + file_location[5:] + "_sol.txt")

            with open("solutions/" + file_location[5:] + "_sol.txt", 'w+') as f:
                f.write(solve_it(input_data, prev_sol))
        else:
            print(solve_it(input_data))

        print("total time: " + str(stopwatch))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
