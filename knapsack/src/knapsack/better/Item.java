package knapsack.better;

/*
 * Created by Adham Ibrahim on 11/9/2020
 */

public class Item implements Comparable<Item> {

    private int value;
    private int weight;

    private int index;

    public Item(int value, int weight, int i) {
        this.value = value;
        this.weight = weight;
        this.index = i;
    }

    @Override
    public int hashCode() {
        return index;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;

        if (! (o instanceof Item)) return false;

        Item i = (Item) o;

        return this.index == i.index;
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
