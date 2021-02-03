#!/usr/bin/python
# -*- coding: utf-8 -*-

from mip_gb import *
from local_search_vrp import solve_subproblems, local_search

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    customer_count = int(parts[0])
    vehicle_count = int(parts[1])
    vehicle_capacity = int(parts[2])

    customers = []
    for i in range(1, customer_count + 1):
        line = lines[i]
        parts = line.split()
        customers.append(Customer(i - 1, int(parts[0]), float(parts[1]), float(parts[2])))

    # the depot is always the first customer in the input
    depot = customers.pop(0)

    '''
    with open("final-solutions/%d_%d" % (customer_count, vehicle_count), "r") as f:
        return f.read()
    '''

    bestobj = 1000000
    bestsol = ""

    # subproblems = read_subproblems("route-info/%d_%d" % (customer_count, vehicle_count), customers)
    for i in range(0, 10000):
        subproblems = get_init_subs_ort(vehicle_count, vehicle_capacity, depot, customers)

        obj, solution = solve_subproblems(depot, subproblems, tsp_iters=20)

        if obj < bestobj:
            bestobj = obj
            bestsol = solution
            with open("solutions/%d_%d" % (customer_count, vehicle_count), "w") as f:
                f.write(("%.4f 0\n" % bestobj) + bestsol)

        print("Iteration:", i, ", bestobj:", bestobj)

    '''
    with open("route-info/%d_%d" % (customer_count, vehicle_count), "w") as f:
        for subproblem in subproblems:
            f.write(" ".join(map(str, (customer.index for customer in subproblem))) + "\n")
    '''

    bestsol = ("%.4f 0\n" % bestobj) + bestsol

    with open("solutions/%d_%d" % (customer_count, vehicle_count), "w") as f:
        f.write(bestsol)

    print(bestsol)

    return solution


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        solution = solve_it(input_data)
        print(solution)
        with open("temp_sol.txt", "w") as f:
            f.write(solution)
    else:

        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)')
