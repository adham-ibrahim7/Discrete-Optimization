#Knapsack

See `handout.pdf` for problem formulation.

Solving the knapsack problem by improving the brute force solution.
A heuristic is used to prune the search space: if the current obtained
value plus an estimate is less than the best obtained value, the 
entire subtree currently being searched can be ignored.

See `knapsack\old` for dynamic programming, which is only efficient for
small knapsack capacities.