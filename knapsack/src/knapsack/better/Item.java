package knapsack.better;

/*
 * Created by Adham Ibrahim on 11/9/2020
 */

public class Item implements Comparable<Item> {

    private int value;
    private int weight;

    public Item(int value, int weight) {
        this.value = value;
        this.weight = weight;
    }

    @Override
    public int hashCode() {
        return 31 * value + weight;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;

        if (! (o instanceof Item)) return false;

        Item i = (Item) o;

        return this.value == i.value && this.weight == i.weight;
    }

    @Override
    public int compareTo(Item o) {
        return -Double.compare((double) this.value / this.weight, (double) o.value / o.weight);
    }

    public int getValue() {
        return this.value;
    }

    public int getWeight() {
        return this.weight;
    }

}
