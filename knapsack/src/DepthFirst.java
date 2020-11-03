/*
 * Created by Adham Ibrahim on 11/2/2020
 */

public class DepthFirst extends BranchAndBound {

    private Node bestSoFar;

    public DepthFirst(Knapsack ks) {
        super(ks);
    }

    protected Node search() {
        solve(0, new Node(0, ks.K(), ks.greedyRelaxation(), null));
        return bestSoFar;
    }

    private void solve(int i, Node current) {
        if (bestSoFar != null && current.estimate < bestSoFar.value ||
                current.room < 0) {
            //this node is worse than the best so far, or it exceeds the capacity
            //there's no point in continuing the search
            return;
        }

        if (i == ks.N()) {
            //done solving this node
            if (bestSoFar == null || current.value > bestSoFar.value) {
                //new best
                bestSoFar = current;
            }
            return;
        }

        //try taking the item
        solve(i+1, new Node(current.value + ks.value(i), current.room - ks.weight(i), current.estimate, current));
        //not taking the item
        solve(i+1, new Node(current.value, current.room, current.estimate - ks.value(i), current));
    }
}
