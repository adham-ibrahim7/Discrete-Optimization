#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from tsp.localsearch_tsp import k_opt, two_opt, two_opt_on_list, reverse
from tsp.util import Point, create_greedy, dist


def solve_it(input_data, input_file=""):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    node_count = int(lines[0])

    coordinates = []
    for i in range(1, node_count + 1):
        line = lines[i]
        parts = line.split()
        coordinates.append(Point(float(parts[0]), float(parts[1])))

    solution_path = "solutions/" + input_file[7:] + ".txt"
    if False: #s.path.exists(solution_path):
        f = open(solution_path, "r")
        best_cost, _ = map(float, f.readline().split())
        best_tour = f.readline().split()
    else:
        best_tour, best_cost = list(range(node_count)), sum(dist(coordinates[i-1], coordinates[i]) for i in range(node_count))

        if node_count < 30000:
            for i in range(200000):
                tour, cost = create_greedy(node_count, coordinates)

                # calculate the length of the tour
                cost = sum(dist(coordinates[tour[i - 1]], coordinates[tour[i]]) for i in range(node_count))

                while True:
                    prev_cost = cost
                    tour, cost = two_opt_on_list(node_count, coordinates, tour, cost)
                    if prev_cost >= cost:
                        break

                if cost < best_cost:
                    best_cost = cost
                    best_tour = tour
                    print(i, best_cost)
                    print(' '.join(map(str, best_tour)))


    # prepare the solution in the specified output format
    output_data = '%.2f' % best_cost + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, best_tour))

    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data, file_location))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)')
