from collections import namedtuple
from random import randint, random

from tsp.util import dist


def reverse(configuration, i, j):
    for k in range(0, (j - i) // 2 + 1):
        configuration[i + k], configuration[j - k] = configuration[j - k], configuration[i + k]


def two_opt(node_count, coordinates, configuration, cost):
    '''
    t2, t4 = randint(0, node_count-1), randint(0, node_count-1)
    t1 = t2 - 1
    t3 = t4 - 1
    '''

    t2 = max(range(0, node_count), key=lambda i: dist(coordinates[configuration[i]], coordinates[configuration[i - 1]]))
    t1 = t2 - 1

    t4 = max(range(0, node_count), key=lambda i: dist(coordinates[configuration[i]], coordinates[configuration[i - 1]]) if i != t2 else 0)
    t3 = t4 - 1

    if t1 > t3:
        t1, t2, t3, t4 = t3, t4, t1, t2

    cost -= dist(coordinates[configuration[t1]], coordinates[configuration[t2]])
    cost -= dist(coordinates[configuration[t3]], coordinates[configuration[t4]])

    reverse(configuration, t2, t3)

    cost += dist(coordinates[configuration[t1]], coordinates[configuration[(t1+1) % node_count]])
    cost += dist(coordinates[configuration[t4-1]], coordinates[configuration[t4]])

    return cost


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
