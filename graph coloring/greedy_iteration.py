from random import shuffle


def greedy(node_count, nodes, adj):
    """
    With a certain ordering of the nodes, perform the greedy coloring algorithm
    """

    color_map = list(-1 for _ in range(node_count))

    for node in nodes:
        neigh_colors = set(color_map[neighbor] for neighbor in adj[node])

        for color in range(node_count):
            if color not in neigh_colors:
                color_map[node] = color
                break

    return color_map


def permute_nodes(node_count, prev_solution, adj):
    """
    Given a solution, group nodes by colors, then within these groups sort by descending degree
    Shuffle these groups and concatenate, then do the greedy solution on this new node ordering
    This process is guaranteed to produce no worse of a solution than the one it is given
    """

    nodes_lists = []
    for color in range(node_count):
        curr_color = list(node for node in range(node_count) if prev_solution[node] == color)
        if len(curr_color) == 0:
            break
        curr_color.sort(key=lambda node: len(adj[node]), reverse=True)
        nodes_lists.append(curr_color)

    shuffle(nodes_lists)

    nodes = []
    for node_list in nodes_lists:
        nodes.extend(node_list)

    return nodes
