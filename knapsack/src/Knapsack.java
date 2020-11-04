
/*
 * Immutable Knapsack type, storing items and its own capacity
 *
 * Created by Adham Ibrahim on Oct 25, 2020
 */

public class Knapsack {
    private final int[] values;
    private final int[] weights;
    private final int K;

    private int greedyRelaxation;
    private double partialRelaxation;

    public Knapsack(final int[] values, final int[] weights, final int K) {
        if (values.length != weights.length)
            throw new IllegalArgumentException("Values and weights do not have same size");

        this.values = values;
        this.weights = weights;
        this.K = K;

        greedyRelaxation = 0;
        partialRelaxation = 0;
        int tempCapacity = K;
        for (int i = 0; i < N(); i++) {
            greedyRelaxation += values[i];
            partialRelaxation += (double) value(i) * Math.min(tempCapacity, weight(i)) / weight(i);
            tempCapacity -= weight(i);
            if (tempCapacity < 0) tempCapacity = 0;
        }
    }

    public int N() {
        return this.values.length;
    }

    public int K() {
        return this.K;
    }

    public int value(int i) {
        return this.values[i];
    }

    public int weight(int i) {
        return this.weights[i];
    }

    public int greedyRelaxation() {
        return greedyRelaxation;
    }

    public int partialValueRelaxation() {
        return (int) partialRelaxation;
    }

}
