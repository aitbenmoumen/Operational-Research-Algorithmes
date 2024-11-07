package com.mycompany.algo;

import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.Edge;
import org.graphstream.graph.implementations.SingleGraph;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.SimpleWeightedGraph;
import org.jgrapht.GraphPath;

import java.util.Random;
import java.util.Scanner;

public class Algo {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        // Create a weighted graph using JGraphT
        SimpleWeightedGraph<String, DefaultWeightedEdge> graph = new SimpleWeightedGraph<>(DefaultWeightedEdge.class);

        // Ask for the number of vertices
        System.out.print("Enter the number of vertices: ");
        int numVertices = scanner.nextInt();
        scanner.nextLine(); // Consume the newline character

        // Generate vertices named x0 to xN
        String[] vertices = new String[numVertices];
        for (int i = 0; i < numVertices; i++) {
            vertices[i] = "x" + i;
            graph.addVertex(vertices[i]);
        }

        // Add edges with random weights between 1 and 100
        System.out.println("Adding edges with random weights between 1 and 100:");
        for (int i = 0; i < numVertices; i++) {
            for (int j = i + 1; j < numVertices; j++) {
                int weight = random.nextInt(100) + 1;
                DefaultWeightedEdge edge = graph.addEdge(vertices[i], vertices[j]);
                graph.setEdgeWeight(edge, weight);
                System.out.println(vertices[i] + " - " + vertices[j] + " : " + weight);
            }
        }

        // Create the graph for visualization using GraphStream
        Graph gsGraph = new SingleGraph("Dijkstra Graph");

        // Add nodes and edges in GraphStream
        for (String vertex : vertices) {
            gsGraph.addNode(vertex).setAttribute("ui.label", vertex);
        }

        for (DefaultWeightedEdge edge : graph.edgeSet()) {
            String source = graph.getEdgeSource(edge);
            String target = graph.getEdgeTarget(edge);
            double weight = graph.getEdgeWeight(edge);

            // Add edges in GraphStream with labels
            Edge gsEdge = gsGraph.addEdge(source + "-" + target, source, target);
            gsEdge.setAttribute("ui.label", String.valueOf(weight));
            gsEdge.setAttribute("weight", weight);
        }

        // Display the graph
        gsGraph.display();

        // Ask for the start and end vertices for Dijkstra
        System.out.print("Enter the starting vertex for Dijkstra (e.g., x0): ");
        String startVertex = scanner.nextLine();
        System.out.print("Enter the ending vertex for Dijkstra (e.g., x1): ");
        String endVertex = scanner.nextLine();

        // Verify the vertices exist in the graph
        if (graph.containsVertex(startVertex) && graph.containsVertex(endVertex)) {
            // Compute the shortest path with Dijkstra
            DijkstraShortestPath<String, DefaultWeightedEdge> dijkstraAlg = new DijkstraShortestPath<>(graph);
            GraphPath<String, DefaultWeightedEdge> path = dijkstraAlg.getPath(startVertex, endVertex);

            if (path != null) {
                System.out.println("Minimum distance from " + startVertex + " to " + endVertex + " : " + path.getWeight());
                System.out.println("Shortest path: " + path.getVertexList());
            } else {
                System.out.println("No path found between " + startVertex + " and " + endVertex);
            }
        } else {
            System.out.println("One of the vertices does not exist in the graph.");
        }

        scanner.close();
    }
}
