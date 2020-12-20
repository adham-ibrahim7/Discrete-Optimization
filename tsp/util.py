from random import shuffle, random, randint

import math
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


def dist(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def create_greedy_permutation(node_count, coordinates):
    permutation = list(range(node_count))
    shuffle(permutation)

    INF = 10000000

    cost = 0
    tour = []
    for node in permutation:
        best_i = 0
        best_cost_delta = INF
        for i in range(len(tour)):
            delta = -dist(coordinates[tour[i]], coordinates[tour[i-1]])
            delta += dist(coordinates[tour[i]], coordinates[node])
            delta += dist(coordinates[tour[i-1]], coordinates[node])
            if delta < best_cost_delta:
                best_cost_delta = delta
                best_i = i
        if best_cost_delta < INF:
            cost += best_cost_delta
        tour.insert(best_i, node)

    return tour, cost


def create_greedy_adj(node_count, coordinates):
    permutation, cost = create_greedy_permutation(node_count, coordinates)
    adj = list([] for _ in range(node_count))

    for i in range(node_count):
        u, v = permutation[i], permutation[i-1]
        adj[u].append(v)
        adj[v].append(u)

    return adj, cost


def convert_adj_to_permutation(node_count, adj):
    tour = [0]
    adj[0].pop()

    while len(tour) < node_count:
        current_node = tour[-1]
        next_node = adj[current_node].pop()
        if current_node in adj[next_node]:
            adj[next_node].remove(current_node)
        tour.append(next_node)
    return tour

'''
def ccw(A,B,C):
    return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)


def intersecting(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)


    # use edge list in local search
    configuration = set((i, (i + 1) % node_count) for i in range(node_count))

    # solve!!
    for _ in range(1):
        two_opt(coordinates, configuration, 0)

    # construct tour from edge list

    adj = list([] for _ in range(node_count))

    for edge in configuration:
        a, b = edge
        adj[a].append(b)
        adj[b].append(a)

    for u in range(node_count):
        print(u, adj[u])

    tour = [0]
    adj[0].pop()

    while len(tour) < node_count:
        current_node = tour[-1]
        next_node = adj[current_node].pop()
        if current_node in adj[next_node]:
            adj[next_node].remove(current_node)
        tour.append(next_node)
        print(tour)
    '''