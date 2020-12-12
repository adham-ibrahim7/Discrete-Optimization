#!/usr/bin/python
# -*- coding: utf-8 -*-

from tsp.localsearch_tsp import k_opt, two_opt
from tsp.util import Point, create_greedy, dist


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    node_count = int(lines[0])

    coordinates = []
    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        coordinates.append(Point(float(parts[0]), float(parts[1])))

    # start with a greedy solution
    configuration = create_greedy(node_count, coordinates)

    # calculate the length of the tour
    cost = sum(dist(coordinates[configuration[i - 1]], coordinates[configuration[i]]) for i in range(node_count))

    print("init cost:", cost)

    # iterate towards local optimum
    for _ in range(1000):
        cost = two_opt(node_count, coordinates, configuration, cost)

    # prepare the solution in the specified output format
    output_data = '%.2f' % cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, configuration))

    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
