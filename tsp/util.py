import math
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])


def dist(point1, point2):
    return math.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)


def create_greedy(node_count, coordinates):
    nodes_left = set(range(1, node_count))

    configuration = [0]
    while len(configuration) < node_count:
        configuration.append(min(nodes_left, key=lambda node: dist(coordinates[node], coordinates[configuration[-1]])))
        nodes_left.remove(configuration[-1])

    return configuration