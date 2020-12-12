# Travelling Salesperson Problem

---

Arguably the most famous optimization problem.

Progress:
- Begin with storing tours as arrays (the end being virtually connected to the beginning), and 
  implementing two opt. This is inefficient mainly because removing edges and adding edges is implicitly
  done by editing the array, namely reversing a certain subarray. This is awkward, and can be improved upon
  
Ideas:
- Instead, store the tour as a set of bidirectional edges. The direction is unimportant until
  the tour has to be outputted, but this can just be done by following each edge. This will allow
  for efficient removal and addition of edges, and should be freer as the direction is what made the 
  array implementation slow.