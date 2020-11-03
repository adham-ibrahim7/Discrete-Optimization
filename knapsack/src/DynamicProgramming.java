
/*
 * Created by Adham Ibrahim on Oct 25, 2020
 */

public class DynamicProgramming extends Solver {

    public DynamicProgramming(Knapsack ks) {
        super(ks);

        long[][] dp = new long[ks.N() + 1][ks.K() + 1];

        for (int i = 1; i <= ks.N(); i++) {
            for (int k = 0; k <= ks.K(); k++) {
                dp[i][k] = dp[i - 1][k];
                if (k - ks.weight(i - 1) >= 0)
                    dp[i][k] = Math.max(dp[i][k], dp[i - 1][k - ks.weight(i - 1)] + ks.value(i - 1));
            }
        }

        objectiveValue = dp[ks.N()][ks.K()];

        int k = ks.K();
        for (int i = ks.N(); i >= 1; i--) {
            taken[i - 1] = dp[i][k] != dp[i - 1][k];
            if (taken[i - 1]) k -= ks.weight(i - 1);
        }
		
		/*for (k = 0; k <= ks.K(); k++) {
			for (int i = 0; i <= ks.N(); i++) {
				System.out.print(dp[i][k] + " ");
			}
			System.out.println();
		}*/
    }

    @Override
    public boolean isGuaranteedOptimal() {
        return true;
    }

}
