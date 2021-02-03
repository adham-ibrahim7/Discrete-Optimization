from tsp.solver import *
import random


def solve_tsp(depot, customers, tsp_iters=10):
    all_points = [depot] + customers

    input_data = "%d \n" % len(all_points)

    for point in all_points:
        input_data += "%d %d\n" % (point.x, point.y)

    lines = solve_it(input_data, iters=tsp_iters).split("\n")
    obj = float(lines[0].split()[0])
    tour_raw = map(int, lines[1].split())

    tour = []
    for i in tour_raw:
        tour.append(str(all_points[i].index))

    return obj, tour


def solve_subproblems(depot, subproblems, tsp_iters=10):
    obj = 0
    solution = ""

    i = 1
    for subproblem in subproblems:
        # print("solving sub %d/%d" % (i, len(subproblems)))
        i += 1

        subobj, tour = solve_tsp(depot, subproblem, tsp_iters=tsp_iters)

        depot_index = tour.index("0")
        tour = tour[depot_index:] + tour[:depot_index] + ["0"]

        obj += subobj
        solution += " ".join(tour) + "\n"

    return obj, solution


def local_search(vehicle_count, vehicle_capacity, depot, subproblems, prevobj):
    suba, subb = random.sample(subproblems, 2)

    totala = sum(customer.demand for customer in suba)
    totalb = sum(customer.demand for customer in subb)

    a, b = random.choice(suba), random.choice(subb)

    print(totala, totalb)
    print(a.demand, b.demand)

    if totala - a.demand + b.demand <= vehicle_capacity and \
        totalb - b.demand + a.demand <= vehicle_capacity:

        print("yuh")

        suba.remove(a)
        subb.remove(b)
        suba.append(b)
        subb.append(a)

        if solve_subproblems(depot, subproblems)[0] < prevobj:
            return subproblems