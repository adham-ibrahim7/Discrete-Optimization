package knapsack.old;
/*
 * Trivial greedy solution, fills as many items in order as possible
 *
 * Created by Adham Ibrahim on Oct 25, 2020
 */

import knapsack.Solver;

public class Greedy extends Solver {

    public Greedy(Knapsack ks) {
        super(ks);

        objectiveValue = 0;
        int weight = 0;

        for (int i = 0; i < ks.N(); i++) {
            if (weight + ks.weight(i) <= ks.K()) {
                taken[i] = true;
                objectiveValue += ks.value(i);
                weight += ks.weight(i);
            } else {
                taken[i] = false;
            }
        }
    }

    @Override
    public boolean isGuaranteedOptimal() {
        return false;
    }

}
