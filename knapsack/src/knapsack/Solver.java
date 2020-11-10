package knapsack;

/*
 * Created by Adham Ibrahim on Oct 25, 2020
 */

import knapsack.old.Knapsack;

public abstract class Solver {

    /**
     * The knapsack the solver computes on
     */
    public final Knapsack ks;
    protected final boolean[] taken;
    /**
     * The objectiveValue computed in the constructor
     */
    protected int objectiveValue;

    /**
     * Constructs generic solver with knapsack
     * @param ks
     */
    public Solver(Knapsack ks) {
        this.ks = ks;

        objectiveValue = 0;
        taken = new boolean[ks.N()];
    }

    public Solver() {
        ks = null;
        taken = null;
    }

    /**
     * Get the objective value computed by the solver
     *
     * @return the objective value
     */
    public int objectiveValue() {
        return objectiveValue;
    }

    /**
     * Did the solver guarantee optimality of the solution?
     *
     * @return true if optimal, false otherwise
     */
    public abstract boolean isGuaranteedOptimal();

    /**
     * Was item i taken or not, in the solution
     *
     * @param i
     * @return true if taken, false otherwise
     */
    public boolean isTaken(int i) {
        return taken[i];
    }

}
