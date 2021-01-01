#!/usr/bin/python
# -*- coding: utf-8 -*-

from facility import *


def solve_it(input_data, file_location=None):
    if file_location is not None:
        return open("./solutions/" + file_location[7:], "r").read()

    return solve_to_file(input_data)


def solve_to_file(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    parts = lines[0].split()
    facility_count = int(parts[0])
    customer_count = int(parts[1])

    facilities = []
    for i in range(1, facility_count + 1):
        parts = lines[i].split()
        facilities.append(Facility(i - 1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3]))))

    customers = []
    for i in range(facility_count + 1, facility_count + 1 + customer_count):
        parts = lines[i].split()
        customers.append(Customer(i - 1 - facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

    # create k * k squares of sub-problems
    k = 5
    all_places = facilities + customers
    dx = (max(o.location.x for o in all_places) - min(o.location.x for o in all_places)) / k + 1000
    dy = (max(o.location.y for o in all_places) - min(o.location.y for o in all_places)) / k + 1000

    bounds = []
    for x in range(0, k):
        for y in range(0, k):
            bounds.append((x * dx, (x + 1) * dx, y * dy, (y + 1) * dy))

    def in_bound(bound, location):
        return bound[0] <= location.x <= bound[1] and bound[2] <= location.y <= bound[3]

    sub_problems = list([[], []] for _ in range(len(bounds)))

    for facility in facilities:
        for j in range(len(bounds)):
            if in_bound(bounds[j], facility.location):
                sub_problems[j][0].append(facility)

    for customer in customers:
        for j in range(len(bounds)):
            if in_bound(bounds[j], customer.location):
                sub_problems[j][1].append(customer)

    # check that every facility and customer is inside of some sub-problem
    print("TOTAL FACILITIES:", sum(len(sub_problem[0]) for sub_problem in sub_problems))
    print("TOTAL CUSTOMERS:", sum(len(sub_problem[1]) for sub_problem in sub_problems))

    # build solution from sub-problems (literally just append sub solutions to each other)
    full_solution = {}
    full_obj = 0
    for i, (facilities, customers) in enumerate(sub_problems):
        print("---- Solving sub-problem", i + 1, "/", len(sub_problems), "----")
        obj, solution = mip(facilities, customers)
        full_obj += obj
        full_solution.update(solution)

    # prepare the solution in the specified output format
    output_data = '%.4f' % full_obj + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, (full_solution[c].index for c in sorted(full_solution))))

    return output_data


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        print("FACILITY LOCATION MIP", file_location)
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        with open("solution.txt", "w") as output_file:
            output_file.write(solve_it(input_data))
    else:
        print(
            'This test requires an input file.  Please select one from the data directory. (i.e. python solver_temp.py ./data/fl_16_2)')
