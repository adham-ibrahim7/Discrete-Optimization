# Graph Coloring

Given a graph, color each node so no adjacent nodes have the same color.
Colors here are represented by numbers 0 ... k-1.

The greedy algorithm is simple as follows:

```
having ordered the nodes in some particular way (see below)

for every node u:
    set neigh_colors to the colors that the previously colored neighbors of u occupy
    color u to the smallest color not in neigh_colors
```

This will clearly produce a feasible solution, but often a terrible one. One simple
optimization to reduce the colors used by such a solution is to order the nodes by
decreasing degree. Intuitively, coloring the nodes that have the most constraints on
them early on will guarantee they are colored as few colors as possible. The nodes with
maybe one neighbor only have to check one color and so are less of a priority.

A surprisingly simple iterative approach can continually reorder the nodes in such
a way that a new solution is no worse than a previous one. Having found a solution,
group the nodes by color, and within each color sort by decreasing degree. Then permute
these groups randomly and append them together to form a new ordering, to be fed to 
the greedy algorithm. 

Why does this work? Each group is a set of nodes that are not adjacent to each other. Randomly
permuting these groups might just append a few nodes to the front and back that are also not
adjacent to any of them, meaning they can all be colored the same. This will slowly reduce
the number of colors, and eventually converge at a local optimum.

This local optimum is usually not the global optimum, at least for large graphs.

TODO:
- Implement local search optima finding. Remove a color, and fix violations until a feasible coloring
 with one less color is found
- Prove optimality

A visualizer that can take a coloring produced by `solver.py` is found here https://discreteoptimization.github.io/vis/coloring/.

Example graphs and some computed colorings are found in `data/` and `solutions/` respectively.