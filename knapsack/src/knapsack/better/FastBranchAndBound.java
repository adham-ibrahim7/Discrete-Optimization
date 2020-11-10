package knapsack.better;

/*
 * Created by Adham Ibrahim on 11/9/2020
 */

import knapsack.Solver;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class FastBranchAndBound extends Solver {

    //TODO obsolete now with fast method
    private static final long MAX_RUNNING_TIME_MILLIS = 100_000;

    private Item[] orig;
    private Item[] items;
    private long capacity;

    private int bestValue;
    private Set<Item> bestSet;

    private final long startTime;

    public FastBranchAndBound(int[] values, int[] weights, long capacity) {
        super();

        startTime = System.currentTimeMillis();

        orig = new Item[values.length];
        items = new Item[values.length];

        for (int i = 0; i < values.length; i++) {
            orig[i] = new Item(values[i], weights[i], i);
            items[i] = new Item(values[i], weights[i], i);
        }

        Arrays.sort(items);

        this.capacity = capacity;

        this.bestSet = new HashSet<>();

        solve(0, 0, capacity, new HashSet<>());
    }

    private void solve(int i, int currentValue, long capacity, Set<Item> takenItems) {
        if (elapsedTime() >= MAX_RUNNING_TIME_MILLIS) {
            return;
        }

        if (currentValue > bestValue) {
            bestValue = currentValue;
            bestSet = takenItems;
        }

        //TODO why cant it deal with more than 5000?
        if (i >= Math.min(5000, items.length)) {
            return;
        }

        double upperBound = currentValue + linearRelaxation(i, capacity);

        if (upperBound <= bestValue) {
            return;
        }

        //with
        if (capacity >= items[i].getWeight()) {
            Set<Item> newTakenItems = new HashSet<>(takenItems);
            newTakenItems.add(items[i]);
            solve(i+1, currentValue + items[i].getValue(), capacity - items[i].getWeight(), newTakenItems);
        }

        //without
        solve(i+1, currentValue, capacity, takenItems);
    }

    private double linearRelaxation(int start, long capacity) {
        double estimate = 0;

        for (int i = start; i < items.length; i++) {
            if (items[i].getWeight() <= capacity) {
                estimate += items[i].getValue();
                capacity -= items[i].getWeight();
            } else {
                estimate += (double) capacity / items[i].getWeight() * items[i].getValue();
                break;
            }
        }

        return estimate;
    }

    @Override
    public int objectiveValue() {
        return bestValue;
    }

    @Override
    public boolean isTaken(int i) {
        return bestSet.contains(orig[i]);
    }

    @Override
    public boolean isGuaranteedOptimal() {
        return elapsedTime() < MAX_RUNNING_TIME_MILLIS + 500;
    }

    private long elapsedTime() {
        return System.currentTimeMillis() - startTime;
    }

}
