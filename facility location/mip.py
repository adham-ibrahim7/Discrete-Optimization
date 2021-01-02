from ortools.linear_solver import pywraplp

from util import *

from itertools import product

import gurobipy as gp
from gurobipy import GRB


def mip_ort(facilities, customers):
    solver = pywraplp.Solver.CreateSolver('SCIP')
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
            dist[facility][customer] = length(facility.location, customer.location)
            serves[facility][customer] = solver.IntVar(0, 1, '')  # if dist[facility][customer] < 50000 else 0
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


def mip_gb(facilities, customers, sub_problem_num):
    cartesian_prod = list(product(customers, facilities))
    setup_cost = {facility: facility.setup_cost for facility in facilities}
    capacities = {facility: facility.capacity for facility in facilities}
    demands = {customer: customer.demand for customer in customers}
    shipping_cost = {(c, f): length(c.location, f.location) for c, f in cartesian_prod}

    m = gp.Model('facility_location')

    select = m.addVars(facilities, vtype=GRB.BINARY, name='select')
    assign = m.addVars(cartesian_prod, vtype=GRB.BINARY, name='assign')

    m.addConstrs((assign[(c, f)] <= select[f] for c, f in cartesian_prod), name='Ship only if you can')
    m.addConstrs((gp.quicksum(assign[(c, f)] for f in facilities) == 1 for c in customers), name='Every customer is satisfied')
    m.addConstrs((gp.quicksum(assign[(c, f)] * demands[c] for c in customers) <= capacities[f] for f in facilities), name='Facility capacity is not met')

    m.setObjective(select.prod(setup_cost) + assign.prod(shipping_cost), GRB.MINIMIZE)
    m.setParam('TimeLimit', 15 * 60)
    # m.setParam('SolFiles', 'temp-solutions/sub_%d_fl_500_7' % sub_problem_num)

    print(m.optimize())

    solution = {}
    for customer in customers:
        for facility in facilities:
            if assign[customer, facility].x > 1e-6:
                solution[customer] = facility
                break

    return m.objVal, solution
