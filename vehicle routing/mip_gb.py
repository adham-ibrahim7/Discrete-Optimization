from itertools import product
import gurobipy as gp
from gurobipy import GRB

from util import *


def gurobi_subproblems(vehicle_count, vehicle_capacity, depot, customers):
    all_points = [depot] + customers
    point_to_vehicle = list(product(all_points, range(vehicle_count)))
    point_to_point = list(product(all_points, all_points))
    demands = {customer: customer.demand for customer in customers}

    m = gp.Model('vrp')

    assign = m.addVars(point_to_vehicle, vtype=GRB.BINARY, name='assign point to vehicle')
    connected = m.addVars(point_to_point, vtype=GRB.BINARY, name='connect points')

    # depot has to be in every route
    m.addConstrs(assign[depot, v] == 1 for v in range(vehicle_count))

    # a customer is only served by one route
    m.addConstrs((gp.quicksum(assign[(c, v)] for v in range(vehicle_count)) == 1 for c in customers))
    # vehicle capacity constraint
    m.addConstrs((gp.quicksum(assign[(c, v)] * demands[c] for c in customers) <= vehicle_capacity for v in range(vehicle_count)))

    # connect points only if they are on the same route
    m.addConstrs(connected[a, b] <= 0.5 * (assign[a, v] + assign[b, v]) for a, b in point_to_point for v in range(vehicle_count))

    # euler tours only
    m.addConstrs((gp.quicksum(connected[a, b] for b in customers) == 2 for a in customers))
    # m.addConstr((gp.quicksum(connected[depot, p] for p in all_points) == 2 * vehicle_count))

    dist = {(a, b): length(a, b) for a, b in point_to_point}
    m.setObjective(connected.prod(dist))

    print(m.optimize())