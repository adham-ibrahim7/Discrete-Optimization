from random import shuffle, choice, random


def greedy(node_count, nodes, adj):
    """
    With a certain ordering of the nodes, perform the greedy coloring algorithm
    """

    color_list = list(-1 for _ in range(node_count))

    for node in nodes:
        available_colors = set(range(node_count))
        for neighbor in adj[node]:
            if color_list[neighbor] > -1:
                neigh_color = color_list[neighbor]
                if neigh_color in available_colors:
                    available_colors.remove(neigh_color)

        color_list[node] = min(available_colors)

    return color_list


def permute_solution(node_count, prev_solution, adj):
    """
    Given a solution, group nodes by colors, then within these groups sort by descending degree
    Shuffle these groups and concatenate, then do the greedy solution on this new node ordering
    This process is guaranteed to produce no worse of a solution than the one it is given
    """

    nodes_lists = []
    for color in range(node_count):
        curr_color = list(node for node in range(node_count) if prev_solution[node] == color)
        curr_color.sort(key=lambda node: len(adj[node]), reverse=True)
        nodes_lists.append(curr_color)

    shuffle(nodes_lists)

    nodes = []
    for node_list in nodes_lists:
        nodes.extend(node_list)

    return greedy(node_count, nodes, adj)


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

    nodes = sorted(list(range(node_count)), key=lambda node: len(adj[node]), reverse=True)
    solution = greedy(node_count, nodes, adj)

    #if node_count == 1000:
    #    solution = read_sol("gc_1000_5_sol.txt")

    iterations = 10000
    for i in range(iterations):
        if i % 10 == 0:
            with open("progress.txt", 'w') as f:
                f.write(str(i) + " iterations, " + str(max(solution) + 1) + " colors")
        solution = permute_solution(node_count, solution, adj)

    return stringify(solution)


def stringify(solution):
    coloring_str = ""
    for c in solution:
        coloring_str += str(c) + " "
    return str(max(solution) + 1) + " 0\n" + coloring_str


def read_sol(file_location):
    with open(file_location, "r") as f:
        f.readline()
        return list(int(s) for s in f.readline().split(" "))


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()

        print_to_file = False

        if print_to_file:
            print("Solving: " + file_location)

            with open("sol.txt", 'w') as f:
                f.write(solve_it(input_data))
        else:
            print(solve_it(input_data))

    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
