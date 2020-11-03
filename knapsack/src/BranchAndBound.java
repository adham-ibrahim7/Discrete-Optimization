
/*
 * Created by Adham Ibrahim on Oct 27, 2020
 */

public abstract class BranchAndBound extends Solver {


    public BranchAndBound(Knapsack ks) {
        super(ks);

        Node best = search();

        objectiveValue = best.value;

        constructSolution(best);
    }

    protected abstract Node search();

    @Override
    public boolean isGuaranteedOptimal() {
        return true;
    }

    /**
     * Taking an optimal node, construct the taken[] array by going back up the tree.
     * @param best the optimal node
     */
    private void constructSolution(Node best) {
        Node temp = best;

        int i = ks.N()-1;
        while (temp.prev != null) {
            taken[i--] = temp.value != temp.prev.value;
            temp = temp.prev;
        }
    }

    protected static class Node {

        protected final int value;
        protected final int room;
        protected final int estimate;
        protected final Node prev;

        Node(final int value, final int room, final int estimate, final Node prev) {
            this.value = value;
            this.room = room;
            this.estimate = estimate;
            this.prev = prev;
        }

    }

}
