package knapsack.old;
/*
 * Immutable knapsack.old.Knapsack type, storing items and its own capacity
 *
 * Created by Adham Ibrahim on Oct 25, 2020
 */

import java.util.Arrays;

public class Knapsack {
    private final int[] value;
    private final int[] weight;
    private final int K;

    private final int greedyRelaxation;
    private final double partialRelaxation;

    public Knapsack(final int[] value, final int[] weight, final int K) {
        if (value.length != weight.length)
            throw new IllegalArgumentException("Values and weights do not have same size");

        this.value = value;
        this.weight = weight;
        this.K = K;

        this.greedyRelaxation = computeGreedyRelaxation();
        this.partialRelaxation = computePartialRelaxation();
    }

    private int computeGreedyRelaxation() {
        int greedyRelaxation = 0;
        for (int i = 0; i < N(); i++) {
            greedyRelaxation += value[i];
        }
        return greedyRelaxation;
    }

    private double computePartialRelaxation() {
        Item[] items = new Item[N()];
        for (int i = 0; i < N(); i++) {
            items[i] = new Item(value[i], weight[i]);
        }

        Arrays.sort(items);

        double partialRelaxation = 0;
        int tempCapacity = K();
        for (Item item : items) {
            if (item.weight <= tempCapacity) {
                partialRelaxation += item.value;
                tempCapacity -= item.weight;
            } else {
                partialRelaxation += (double) tempCapacity / item.weight * item.value;
            }
        }

        return partialRelaxation;
    }

    public int N() {
        return this.value.length;
    }

    public int K() {
        return this.K;
    }

    public int value(int i) {
        return this.value[i];
    }

    public int weight(int i) {
        return this.weight[i];
    }

    public int greedyRelaxation() {
        return greedyRelaxation;
    }

    public double partialValueRelaxation() {
        return partialRelaxation;
    }

    private class Item implements Comparable<Item> {
        int value, weight;
        Item(int value, int weight) {
            this.value = value;
            this.weight = weight;
        }

        @Override
        public int compareTo(Item o) {
            return -Double.compare((double) this.value / this.weight, (double) o.value / o.weight);
        }
    }

}
