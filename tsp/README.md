# Travelling Salesperson Problem

Arguably the most famous optimization problem.

Progress:
  - Begin with storing tours as arrays (the end being virtually connected to the beginning), and 
  implementing two opt. This is inefficient mainly because removing edges and adding edges is implicitly
  done by editing the array, namely reversing a certain subarray. This is awkward, and can be improved upon
  - Brute force two opt checking every pair of edges
  
Possible Improvements:
  - doubly linked list to O(1) reverse
  - improve by precomputing which edges are less than some length r and only considering those for swaps
  - get k-opt working?