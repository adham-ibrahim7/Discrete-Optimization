import math
from collections import namedtuple

from ortools.linear_solver import pywraplp

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])


def length(a: Point, b: Point):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def trivial(facilities, customers):
    # build a trivial solution
    # pack the facilities one by one until all the customers are served
    solution = [-1] * len(customers)
    capacity_remaining = [f.capacity for f in facilities]

    facility_index = 0
    for customer in customers:
        if capacity_remaining[facility_index] >= customer.demand:
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand
        else:
            facility_index += 1
            assert capacity_remaining[facility_index] >= customer.demand
            solution[customer.index] = facility_index
            capacity_remaining[facility_index] -= customer.demand

    used = [0] * len(facilities)
    for facility_index in solution:
        used[facility_index] = 1

    # calculate the cost of the solution
    obj = sum([f.setup_cost * used[f.index] for f in facilities])
    for customer in customers:
        obj += length(customer.location, facilities[solution[customer.index]].location)

    return obj, solution


def mip(facilities, customers):
    print("Facilities:", len(facilities), ", Customers:", len(customers))

    solver = pywraplp.Solver.CreateSolver('SCIP')
    # solver = pywraplp.Solver('Solver', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    # solver.SetTimeLimit(15 * 60 * 1000)

    open = {}
    for facility in facilities:
        open[facility] = solver.IntVar(0, 1, '')

    dist = {}
    serves = {}
    for facility in facilities:
        serves[facility] = {}
        dist[facility] = {}
        for customer in customers:
            serves[facility][customer] = solver.IntVar(0, 1, '')
            dist[facility][customer] = length(facility.location, customer.location)
            # a facility can only serve if it is open
            solver.Add(serves[facility][customer] <= open[facility])

        # customer demands dont exceed capacity
        solver.Add(sum(serves[facility][customer] * customer.demand for customer in customers) <= facility.capacity)

    for customer in customers:
        # a customer is served by exactly one facility
        solver.Add(sum(serves[facility][customer] for facility in facilities) == 1)

    solver.Minimize(
        sum(open[facility] * facility.setup_cost +
            sum(serves[facility][customer] * dist[facility][customer] for customer in customers)
            for facility in facilities)
    )

    solver_parameters = pywraplp.MPSolverParameters()
    solver_parameters.SetDoubleParam(pywraplp.MPSolverParameters.PRIMAL_TOLERANCE, 0.0001)

    solver.Solve(solver_parameters)

    solution = {}
    for customer in customers:
        # print("Customer", "%2d" % customer.index, ":", " ".join(map(str, map(int, (serves[facility][customer].solution_value() for facility in facilities)))))
        for facility in facilities:
            if serves[facility][customer].solution_value():
                solution[customer] = facility
                break

    print("-----Problem solved in-----")
    print('%.3f seconds' % (solver.wall_time() / 1000))
    print('%d iterations' % solver.iterations())
    print('%d branch-and-bound nodes' % solver.nodes())

    return solver.Objective().Value(), solution
