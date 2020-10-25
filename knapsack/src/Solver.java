
/*
 * Abstract type with methods for 
 * 
 * Created by Adham Ibrahim on Oct 25, 2020
 */

public abstract class Solver {
	
	/**
	 * The knapsack the solver computes on
	 */
	protected final Knapsack ks;
	
	/**
	 * Constructs generic solver with knapsack
	 * @param ks
	 */
	public Solver(Knapsack ks) {
		this.ks = ks;
	}
	
	/**
	 * Get the objective value computed by the solver
	 * @return the objective value
	 */
	public abstract long objectiveValue();
	
	/**
	 * Did the solver guarantee optimality of the solution?
	 * @return true if optimal, false otherwise
	 */
	public abstract boolean isGuaranteedOptimal();
	
	/**
	 * Was item i taken or not, in the solution
	 * @param i
	 * @return true if taken, false otherwise
	 */
	public abstract boolean isTaken(int i);
	
}
