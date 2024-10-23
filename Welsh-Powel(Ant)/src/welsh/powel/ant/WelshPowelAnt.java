/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Main.java to edit this template
 */
package welsh.powel.ant;
import org.jgrapht.Graph;
import org.jgrapht.graph.SimpleGraph;
import org.jgrapht.alg.color.GreedyColoring;
import org.jgrapht.alg.color.Coloring;
import java.util.Random;
import org.apache.commons.math3.combinatorics.Combinations;
/**
 *
 * @author aaitb
 */
public class WelshPowelAnt {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // Create a simple graph
        Graph<Integer, DefaultEdge> graph = new SimpleGraph<>(DefaultEdge.class);

        // Add vertices
        for (int i = 0; i < 10; i++) {
            graph.addVertex(i);
        }

        // Add edges randomly
        Random random = new Random();
        for (int i = 0; i < 20; i++) {
            int v1 = random.nextInt(10);
            int v2 = random.nextInt(10);
            if (v1 != v2 && !graph.containsEdge(v1, v2)) {
                graph.addEdge(v1, v2);
            }
        }

        // Apply Welsh-Powell algorithm
        Coloring<Integer> coloring = new GreedyColoring<>(graph);
        coloring.color();

        // Print the colors assigned to each vertex
        for (Integer vertex : graph.vertexSet()) {
            System.out.println("Vertex " + vertex + " has color " + coloring.getColor(vertex));
        }
    }
    
}
