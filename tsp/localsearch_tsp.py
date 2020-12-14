from collections import namedtuple
from random import randint, random

from tsp.util import dist


def reverse(configuration, i, j):
    for k in range(0, (j - i) // 2 + 1):
        configuration[i + k], configuration[j - k] = configuration[j - k], configuration[i + k]
    return configuration


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
        for d in range(b+1, node_count):
            a = b-1
            c = d-1
            delta = -_dist(a, b) - _dist(c, d) + _dist(a, c) + _dist(b, d)
            if delta < best_delta:
                best_delta = delta
                best_b, best_d = b, d

    b, d = best_b, best_d
    a, c = b-1, d-1

    if a > c:
        a, b, c, d = c, d, a, b

    cost -= _dist(a, b)
    cost -= _dist(c, d)

    configuration = reverse(configuration, b, c)

    cost += _dist(a, (a+1)%node_count)
    cost += _dist(d-1, d)

    return configuration, cost


def _dist(edge, coordinates):
    return dist(coordinates[edge[0]], coordinates[edge[1]])


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

    return cost - _dist(edge1, coordinates) - _dist(edge2, coordinates) + _dist((a, d), coordinates) + _dist((c, b), coordinates)


def k_opt(node_count, coordinates, outbound, inbound):
    t1 = max(range(node_count), key=lambda node: dist(coordinates[node], coordinates[outbound[node]]))
    t2 = outbound[t1]

    t3 = min(range(node_count), key=lambda node: dist(coordinates[node], coordinates[t2]) if node != t2 else 1000000)
    if dist(coordinates[t2], coordinates[t3]) < dist(coordinates[t1], coordinates[t2]):
        t4 = inbound[t3]
        outbound[t3] = t2
        inbound[t2] = t3
        outbound[t1] = t4
        inbound[t4] = t1

    print(t1, t2, t3, t4)

    return outbound, inbound
