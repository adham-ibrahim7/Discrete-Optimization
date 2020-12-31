#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from ortools.linear_solver import pywraplp

Item = namedtuple("Item", ['index', 'value', 'weight'])


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    solver = pywraplp.Solver.CreateSolver('SCIP')

    taken = {}
    for item in items:
        taken[item] = solver.IntVar(0, 1, '')

    solver.Add(sum(taken[item] * item.weight for item in items) <= capacity)
    solver.Maximize(sum(taken[item] * item.value for item in items))

    # lower tolerance for better solution?
    solver_parameters = pywraplp.MPSolverParameters()
    solver_parameters.SetDoubleParam(pywraplp.MPSolverParameters.PRIMAL_TOLERANCE, 0.00001)
    solver.Solve(solver_parameters)

    solution = []

    for item in items:
        solution.append(taken[item].solution_value())
    
    # prepare the solution in the specified output format
    output_data = str(int(solver.Objective().Value())) + ' ' + str(0) + '\n'
    output_data += ' '.join(str(int(c)) for c in solution)
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

