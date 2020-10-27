import java.io.*;
import java.util.List;
import java.util.ArrayList;

/**
 * The class <code>Solver</code> is an implementation of a greedy algorithm to
 * solve the knapsack problem.
 *
 */
public class Main {
	
	public static void main(String[] args) {
		try {
			//input, solve, output
			
			Knapsack ks = getInput(args);
			
			Solver solver;
			
			if (ks.K() * ks.N() < 1000000000)
				solver = new DynamicProgramming(ks);
			else
				solver = new Greedy(ks);
			
			output(solver);
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	/**
	 * Read the instance, solve it, and print the solution in the standard output
	 */
	private static Knapsack getInput(String[] args) throws IOException {
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
		int capacity = Integer.parseInt(firstLine[1]);

		int[] values = new int[items];
		int[] weights = new int[items];

		for (int i = 1; i < items + 1; i++) {
			String line = lines.get(i);
			String[] parts = line.split("\\s+");

			values[i - 1] = Integer.parseInt(parts[0]);
			weights[i - 1] = Integer.parseInt(parts[1]);
		}
		
		return new Knapsack(values, weights, capacity);
	}
	
	private static void output(Solver solver) {
		// prepare the solution in the specified output format
		System.out.println(solver.objectiveValue() + " " + (solver.isGuaranteedOptimal() ? 1 : 0));
		for (int i = 0; i < solver.ks.N(); i++) {
			System.out.print((solver.isTaken(i) ? 1 : 0) + " ");
		}
		System.out.println("");
	}
	
}