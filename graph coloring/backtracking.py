def constrain(i, adj, coloring, c):
    for j in adj[i]:
        if not type(coloring[j]) is int and c in coloring[j]:
            coloring[j].remove(c)
    return coloring


calls = 0

'''
    global calls
    for max_color in range(5, 15):
        print("----" + str(max_color) + " colors----")
        coloring, uncolored = [list(range(max_color)) for _ in range(node_count)], list(range(node_count))
        success, solution = backtrack(node_count, adj, coloring, uncolored)

        print(str(calls) + " calls")
        calls = 0

        if success:
            return solution
    '''


def backtrack(nodes, adj, coloring, uncolored):
    global calls

    if calls == 5_000_000:
        return False, None

    calls += 1

    if len(uncolored) == 0:
        return True, coloring

    (_, _, uncolored_node, index) = min(
        (len(coloring[uncolored_node]), len(adj[uncolored_node]), uncolored_node, index) for (index, uncolored_node) in
        enumerate(uncolored))

    domain = coloring[uncolored_node].copy()
    # shuffle(domain)
    for c in domain:
        coloring[uncolored_node] = c
        next_success, solution = backtrack(nodes, adj, constrain(uncolored_node, adj, deepcopy(coloring), c),
                                           uncolored[:index] + uncolored[index + 1:])
        if next_success:
            return True, solution
        coloring[uncolored_node] = domain
    return False, None
