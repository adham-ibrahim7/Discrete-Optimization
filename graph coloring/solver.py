import os
from stopwatch import Stopwatch
from greedy_iteration import greedy, permute_nodes


def solve_it(input_data, prev_sol=None, iterations=10000):
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

        iterations = 10000
        output_file = None

        if len(sys.argv) > 2:
            if sys.argv[2].isnumeric():
                iterations = int(sys.argv[2])
            else:
                output_file = sys.argv[2].strip()

        if len(sys.argv) > 3:
            iterations = int(sys.argv[3])

        print_to_file = False #output_file is not None

        stopwatch = Stopwatch()
        if print_to_file:
            print("Solving: " + file_location)

            prev_sol = read_sol("solutions/" + file_location[5:] + "_sol.txt")

            with open("solutions/" + output_file, 'w+') as f:
                f.write(solve_it(input_data))
        else:
            print(solve_it(input_data))

        print("total time: " + str(stopwatch))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')
