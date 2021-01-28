from ortools.linear_solver import pywraplp

from tsp.solver import *
from tsp.util import *

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])


def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x) ** 2 + (customer1.y - customer2.y) ** 2)


def solve_tsp(depot, customers):
    all_points = [depot] + customers

    input_data = "%d \n" % len(all_points)

    for point in all_points:
        input_data += "%d %d\n" % (point.x, point.y)

    lines = solve_it(input_data, iters=1000).split("\n")
    obj = float(lines[0].split()[0])
    tour_raw = map(int, lines[1].split())

    tour = []
    for i in tour_raw:
        tour.append(str(all_points[i].index))

    return obj, tour


def trivial(vehicle_count, customer_count, vehicle_capacity,
            depot, customers):
    # build a trivial solution
    # assign customers to vehicles starting by the largest customer demands
    vehicle_tours = []

    remaining_customers = set(customers)
    remaining_customers.remove(depot)

    for v in range(0, vehicle_count):
        # print "Start Vehicle: ",v
        vehicle_tours.append([])
        capacity_remaining = vehicle_capacity
        while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
            used = set()
            order = sorted(remaining_customers, key=lambda customer: -customer.demand * customer_count + customer.index)
            for customer in order:
                if capacity_remaining >= customer.demand:
                    capacity_remaining -= customer.demand
                    vehicle_tours[v].append(customer)
                    # print '   add', ci, capacity_remaining
                    used.add(customer)
            remaining_customers -= used

    # checks that the number of customers served is correct
    assert sum([len(v) for v in vehicle_tours]) == len(customers) - 1

    # calculate the cost of the solution; for each vehicle the length of the route
    obj = 0
    for v in range(0, vehicle_count):
        vehicle_tour = vehicle_tours[v]
        if len(vehicle_tour) > 0:
            obj += length(depot, vehicle_tour[0])
            for i in range(0, len(vehicle_tour) - 1):
                obj += length(vehicle_tour[i], vehicle_tour[i + 1])
            obj += length(vehicle_tour[-1], depot)

    # prepare the solution in the specified output format
    outputData = '%.2f' % obj + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(depot.index) + ' ' + ' '.join(
            [str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(depot.index) + '\n'

    return outputData


def get_subproblems(vehicle_count, vehicle_capacity, depot, customers):
    shuffle(customers)

    in_route = {}

    solver = pywraplp.Solver.CreateSolver('SCIP')
    for customer in customers:
        for v in range(vehicle_count):
            in_route[customer, v] = solver.IntVar(0, 1, '')

        # only in one route
        solver.Add(sum(in_route[customer, v] for v in range(vehicle_count)) == 1)

    for v in range(vehicle_count):
        solver.Add(sum(in_route[customer, v] * customer.demand for customer in customers) <= vehicle_capacity)

    '''
    objective = 0
    for v in range(vehicle_count):
        subproblems = []
        for customer in customers:
            if in_route[customer, v]:
                subproblems.append(customer)
        objective += create_greedy_permutation(len(customers), customers)[1]

    solver.Minimize(objective)
    '''

    solver_parameters = pywraplp.MPSolverParameters()
    solver_parameters.SetDoubleParam(pywraplp.MPSolverParameters.PRIMAL_TOLERANCE, 0.0001)
    solver.Solve(solver_parameters)

    subproblems = [[] for _ in range(vehicle_count)]

    for v in range(vehicle_count):
        for customer in customers:
            if in_route[customer, v].solution_value():
                subproblems[v].append(customer)

    return subproblems


def read_subproblems(file, customers):
    by_index = {}
    for customer in customers:
        by_index[customer.index] = customer

    subproblems = []
    with open(file, "r") as f:
        lines = f.read().split("\n")
        for line in lines[:-1]:
            subproblems.append(list(by_index[i] for i in map(int, line.split())))
    return subproblems
