import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Scanner;
import java.util.Random;
public class geminiList {


    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);

        System.out.print("Type how many nodes do you want in your graph: ");
        int nodes = scan.nextInt();

        System.out.println("How many arcs (edges) do you want in your graph? ");
        int arcs = scan.nextInt();

        // Validate user input for arcs (should not exceed n(n-1)/2 for undirected graphs)
        if (arcs > nodes * (nodes - 1) / 2) {
            System.out.println("Error: Number of arcs cannot exceed n(n-1)/2 for an undirected graph.");
            return;
        }

        // Create an ArrayList to represent the adjacency list
        ArrayList<LinkedList<Integer>> adjList = new ArrayList<>(nodes);

        // Initialize each element of the adjacency list with an empty LinkedList
        for (int i = 0; i < nodes; i++) {
            adjList.add(new LinkedList<>());
        }

        Random random = new Random();

        // Add edges (arcs) to the adjacency list
        for (int i = 0; i < arcs; i++) {
            int source = random.nextInt(nodes); // Source node
            int destination = random.nextInt(nodes); // Destination node (avoid self-loops)

            // Avoid duplicate edges and self-loops
            if (source != destination && !adjList.get(source).contains(destination)) {
                adjList.get(source).add(destination);
            } else {
                i--; // Decrement loop counter if edge is invalid (duplicate or self-loop)
            }
        }

        // Print the adjacency list representation of the graph
        for (int i = 0; i < nodes; i++) {
            System.out.print("Node " + i + ": ");
            for (int neighbor : adjList.get(i)) {
                System.out.print(neighbor + " ");
            }
            System.out.println();
        }
    }
}

