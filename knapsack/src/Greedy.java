
/*
 * Trivial greedy solution, fills as many items in order as possible
 * 
 * Created by Adham Ibrahim on Oct 25, 2020
 */

public class Greedy extends Solver {

	private int value;
	private final boolean[] taken;
	
	public Greedy(Knapsack ks) {
		super(ks);

		value = 0;
		int weight = 0;
		taken = new boolean[ks.N()];

		for (int i = 0; i < ks.N(); i++) {
			if (weight + ks.weight(i) <= ks.K()) {
				taken[i] = true;
				value += ks.value(i);
				weight += ks.weight(i);
			} else {
				taken[i] = false;
			}
		}
	}

	@Override
	public long objectiveValue() {
		return value;
	}

	@Override
	public boolean isGuaranteedOptimal() {
		return false;
	}

	@Override
	public boolean isTaken(int i) {
		return taken[i];
	}

}
