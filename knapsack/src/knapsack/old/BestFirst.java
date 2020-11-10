package knapsack.old;/*
 * Created by Adham Ibrahim on 11/2/2020
 */

import java.util.PriorityQueue;
import java.util.Queue;

public class BestFirst extends BranchAndBound {

    public BestFirst(Knapsack ks) {
        super(ks);
    }

    @Override
    protected void search() {
        Queue<BranchAndBound.Node> queue = new PriorityQueue<>();
        queue.add(new BranchAndBound.Node(0, ks.K(), (int) (1.8 * ks.partialValueRelaxation()), 0, null));

        while (!queue.isEmpty()) {
            if (System.currentTimeMillis() - startTime > MAX_RUNNING_TIME_MILLIS) break;

            BranchAndBound.Node current = queue.poll();
            prune(current, queue);
        }
    }

}
