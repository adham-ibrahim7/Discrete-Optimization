from random import randint


def reduce_one(node_count, solution, colors_used):
    for node in range(node_count):
        if solution[node] == colors_used-1:
            solution[node] = randint(0, colors_used-2)
