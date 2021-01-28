from collections import namedtuple
from random import randint, random

from tsp.util import dist, create_greedy_permutation, Point


def reverse(configuration, i, j):
    for k in range(0, (j - i) // 2 + 1):
        configuration[i + k], configuration[j - k] = configuration[j - k], configuration[i + k]
    return configuration


def _dist(edge, coordinates):
    return dist(coordinates[edge[0]], coordinates[edge[1]])


def two_opt_on_list(node_count, coordinates, configuration, cost):
    def _dist(i, j):
        return dist(coordinates[configuration[i]], coordinates[configuration[j]])

    '''
    b = max(range(0, node_count), key=lambda i: _dist(i, i-1))
    a = b - 1

    d = max(range(0, node_count), key=lambda i: _dist(i, i-1) if i != b else 0)
    c = d - 1
    '''

    '''
    '''
    best_b, best_d, best_delta = 0, 0, 0
    for b in range(node_count):
        for d in range(b + 1, node_count):
            a = b - 1
            c = d - 1
            delta = -_dist(a, b) - _dist(c, d) + _dist(a, c) + _dist(b, d)
            if delta < best_delta:
                best_delta = delta
                best_b, best_d = b, d

    b, d = best_b, best_d
    a, c = b - 1, d - 1

    if a > c:
        a, b, c, d = c, d, a, b

    cost -= _dist(a, b)
    cost -= _dist(c, d)

    configuration = reverse(configuration, b, c)

    cost += _dist(a, (a + 1) % node_count)
    cost += _dist(d - 1, d)

    return configuration, cost


def two_opt(coordinates, configuration, cost):
    edge1 = max(configuration, key=lambda edge: _dist(edge, coordinates))
    edge2 = max(configuration, key=lambda edge: _dist(edge, coordinates) if edge != edge1 else 0)

    print(edge1, edge2)

    a, b = edge1
    c, d = edge2

    configuration.remove(edge1)
    configuration.remove(edge2)
    configuration.add((a, d))
    configuration.add((b, c))

    return cost - _dist(edge1, coordinates) - _dist(edge2, coordinates) + _dist((a, d), coordinates) + _dist((c, b),
                                                                                                             coordinates)


def k_opt(node_count, coordinates, adj, cost):
    def disconnect(a, b):
        adj[a].remove(b)
        adj[b].remove(a)

    def connect(a, b):
        adj[a].append(b)
        adj[b].append(a)

    t1 = max(range(node_count), key=lambda node: dist(coordinates[node], coordinates[adj[node][0]]))
    t2 = adj[t1][0]

    print("T1T2", t1, t2)

    disconnect(t1, t2)

    for _ in range(1):
        for t3 in range(node_count):
            if dist(coordinates[t2], coordinates[t3]) < dist(coordinates[t1], coordinates[t2]):
                break
        else:
            # no such t3 exists, complete
            break

        t4 = adj[t3][0] if adj[t3][0] != t2 else adj[t3][1]
        disconnect(t3, t4)
        connect(t2, t3)
        t2 = t4

        print("T3T4", t3, t4)

        # TODO DIRECTED EDGES! (but like ... reverse them right so yeah lol)

    connect(t1, t2)

    return adj, cost


def local_search(node_count, coordinates, greedy_function, search_function, iterations):
    """
    Perform local search with a particular initial greedy configuration function and a search function,
    a function that given a configuration produces another that is no worse. The search performs random restarts, finding
    local optima and updating the best tour ever found.

    The tour representation returned by the greedy function is the same representation expected by the search.
    """

    best_configuration, best_cost = greedy_function(node_count, coordinates)

    for _ in range(iterations):
        tour, cost = greedy_function(node_count, coordinates)

        while True:
            prev_cost = cost
            tour, cost = search_function(node_count, coordinates, tour, cost)
            if prev_cost >= cost:
                break

        if cost < best_cost:
            best_cost = cost
            best_configuration = tour

            print(best_cost)
            with open("temp_sol.txt", "w") as f:
                f.write(str(best_cost) + " 0\n")
                f.write(' '.join(map(str, best_configuration)))

    return best_configuration, best_cost
