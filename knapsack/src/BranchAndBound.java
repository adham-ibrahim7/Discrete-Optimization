
/*
 * Created by Adham Ibrahim on Oct 27, 2020
 */

import java.util.Collection;

public abstract class BranchAndBound extends Solver {

    protected final int MAX_RUNNING_TIME_MILLIS = 120_000;
    protected final long startTime;

    private Node bestSoFar;
    private int updates = 0, totalExplored = 0;

    public BranchAndBound(Knapsack ks) {
        super(ks);

        System.out.println(ks.greedyRelaxation());
        System.out.println(ks.partialValueRelaxation());

        startTime = System.currentTimeMillis();

        bestSoFar = null;
        search();
        objectiveValue = bestSoFar.value;
        constructSolution(bestSoFar);

        System.out.println("FULL SOLUTIONS FOUND: " + totalExplored);
        System.out.println("TIMES BEST SOLUTION IS UPDATED: " + updates);
    }

    //TODO have subclasses give a data structure to this class, and just run search here

    /**
     * Search through the space of all solutions, determine the optimal one.
     */
    protected abstract void search();

    @Override
    public boolean isGuaranteedOptimal() {
        return System.currentTimeMillis() - startTime < MAX_RUNNING_TIME_MILLIS - 500;
    }

    /**
     * Taking an optimal node, construct the taken[] array by going back up the tree.
     * @param solutionNode the optimal node
     */
    private void constructSolution(Node solutionNode) {
        Node temp = solutionNode;

        int i = ks.N()-1;
        while (temp.prev != null) {
            taken[i--] = temp.value != temp.prev.value;
            temp = temp.prev;
        }
    }

    protected void prune(Node current, Collection<Node> searchStructure) {
        if (bestSoFar != null && current.estimate < bestSoFar.value ||
                current.room < 0) {
            //this node is worse than the best so far, or it exceeds the capacity
            //there's no point in continuing the search
            return;
        }

        if (current.i == ks.N()) {
            totalExplored++;
            //done solving this node
            if (bestSoFar == null || current.value > bestSoFar.value) {
                //new best
                bestSoFar = current;
                updates++;
            }
            return;
        }

        //randomize which order the search continues, speeding up significantly in the case of malicious search spaces

        Node without = new Node(current.value, current.room, current.estimate - ks.value(current.i), current.i+1, current);
        Node with = new Node(current.value + ks.value(current.i), current.room - ks.weight(current.i), current.estimate, current.i+1, current);

        if (Math.random() < 0.5) {
            searchStructure.add(without);
            searchStructure.add(with);
        } else {
            searchStructure.add(with);
            searchStructure.add(without);
        }

        //searchStructure.add(with);
        //searchStructure.add(without);
    }

    protected static class Node implements Comparable<Node> {

        protected final int value;
        protected final int room;
        protected final int estimate;
        protected int i;

        protected final Node prev;

        Node(final int value, final int room, final int estimate, final int i, final Node prev) {
            this.value = value;
            this.room = room;
            this.estimate = estimate;
            this.prev = prev;
            this.i = i;
        }

        @Override
        public int compareTo(Node o) {
            return Integer.compare(this.estimate, o.estimate);
        }
    }

}
