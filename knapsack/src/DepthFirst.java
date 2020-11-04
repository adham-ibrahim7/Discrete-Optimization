/*
 * Created by Adham Ibrahim on 11/2/2020
 */

import java.util.Stack;

public class DepthFirst extends BranchAndBound {

    public DepthFirst(Knapsack ks) {
        super(ks);
    }

    @Override
    protected void search() {
        Node bestSoFar = null;

        Stack<Node> stack = new Stack<>();
        stack.add(new Node(0, ks.K(), ks.greedyRelaxation(), 0, null));

        while (!stack.isEmpty()) {
            if (System.currentTimeMillis() - startTime > MAX_RUNNING_TIME_MILLIS) break;

            Node current = stack.pop();
            prune(current, stack);
        }
    }

}
