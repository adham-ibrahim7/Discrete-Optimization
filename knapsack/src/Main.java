import knapsack.Solver;
import knapsack.better.FastBranchAndBound;
import knapsack.old.DynamicProgramming;
import knapsack.old.Knapsack;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * The class <code>knapsack.Solver</code> is an implementation of a greedy algorithm to
 * solve the knapsack problem.
 */
public class Main {

    private static int[] values, weights;
    private static int capacity;

    public static void main(String[] args) {
        try {
            //input, solve, output

            getInput(args);

            Solver solver = new FastBranchAndBound(values, weights, capacity);
            //new DynamicProgramming(new Knapsack(values, weights, capacity));

            output(solver);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * Read the instance, solve it, and print the solution in the standard output
     */
    private static void getInput(String[] args) throws IOException {
        String fileName = null;

        // get the temp file name
        for (String arg : args) {
            if (arg.startsWith("-file=")) {
                fileName = arg.substring(6);
            }
        }
        if (fileName == null)
            throw new IOException("No file is given for input");

        // read the lines out of the file
        List<String> lines = new ArrayList<String>();

        BufferedReader input = new BufferedReader(new FileReader(fileName));
        try {
            String line = null;
            while ((line = input.readLine()) != null) {
                lines.add(line);
            }
        } finally {
            input.close();
        }

        // parse the data in the file
        String[] firstLine = lines.get(0).split("\\s+");
        int items = Integer.parseInt(firstLine[0]);

        capacity = Integer.parseInt(firstLine[1]);

        values = new int[items];
        weights = new int[items];

        for (int i = 1; i < items + 1; i++) {
            String line = lines.get(i);
            String[] parts = line.split("\\s+");

            values[i - 1] = Integer.parseInt(parts[0]);
            weights[i - 1] = Integer.parseInt(parts[1]);
        }
    }

    private static void output(Solver solver) {
        // prepare the solution in the specified output format
        System.out.println(solver.objectiveValue() + " " + (solver.isGuaranteedOptimal() ? 1 : 0));

        for (int i = 0; i < values.length; i++) {
            System.out.print((solver.isTaken(i) ? 1 : 0) + " ");
        }

        System.out.println();
    }

}