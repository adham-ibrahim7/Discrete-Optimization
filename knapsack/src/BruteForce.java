
/*
 * INCOMPLETE
 * 
 * Created by Adham Ibrahim on Oct 27, 2020
 */

public class BruteForce extends Solver {

	public BruteForce(Knapsack ks) {
		super(ks);
		
		objectiveValue = solve(0, ks.K());
	}
	
	private int solve(int i, int weight) {
		if (weight < 0) return Integer.MIN_VALUE;
		if (i == ks.N()) return 0;
		
		int without = solve(i+1, weight);
		int with = solve(i+1, weight - ks.weight(i)) + ks.value(i);
		
		taken[i] = with > without;
		
		return Math.max(with, without);
	}

	@Override
	public boolean isGuaranteedOptimal() {
		return true;
	}

}
