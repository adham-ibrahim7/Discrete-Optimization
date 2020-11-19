from copy import deepcopy


def constrain(i, adj, coloring, c):
    for j in adj[i]:
        if type(coloring[j]) is list and c in coloring[j]:
            coloring[j].remove(c)
    return coloring


def color(nodes, adj, coloring, uncolored):
    if len(uncolored) == 0:
        return True, coloring

    i = uncolored[0]

    domain = coloring[i].copy()
    for c in domain:
        coloring[i] = c
        next_success, solution = color(nodes, adj, constrain(i, adj, deepcopy(coloring), c), uncolored[1:])
        if next_success:
            return True, solution
        coloring[i] = domain
    return False, None


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
    # print(adj)

    for max_color in range(10):
        print(max_color)
        coloring, uncolored = [list(range(max_color)) for _ in range(node_count)], list(range(node_count))
        success, solution = color(node_count, adj, coloring, uncolored)
        if success:
            return solution


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        with open("sol.txt", 'w') as f:
            solution = solve_it(input_data)

            coloring_str = ""
            num_colors = 0
            for c in solution:
                coloring_str += str(c) + " "
                num_colors = max(num_colors, c)

            f.write(str(num_colors + 1) + " 1\n")
            f.write(coloring_str + "\n")
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
