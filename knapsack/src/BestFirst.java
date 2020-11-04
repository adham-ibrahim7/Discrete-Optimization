/*
 * Created by Adham Ibrahim on 11/2/2020
 */

import java.util.PriorityQueue;
import java.util.Queue;
import java.util.Stack;

public class BestFirst extends BranchAndBound {

    public BestFirst(Knapsack ks) {
        super(ks);
    }

    @Override
    protected void search() {
        Node bestSoFar = null;

        Queue<Node> queue = new PriorityQueue<>();
        queue.add(new Node(0, ks.K(), ks.greedyRelaxation(), 0, null));

        while (!queue.isEmpty()) {
            if (System.currentTimeMillis() - startTime > MAX_RUNNING_TIME_MILLIS) break;

            Node current = queue.poll();
            prune(current, queue);
        }
    }

}
