/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.implementation_algo_bellman_ford;
 
import org.graphstream.graph.Graph;
import org.graphstream.graph.Node;
import org.graphstream.graph.Edge;
import org.graphstream.graph.implementations.SingleGraph;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.SimpleDirectedWeightedGraph;
import org.jgrapht.GraphPath;

import java.util.Random;
import java.util.Scanner;

public class Implementation_algo_bellman_ford {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Random random = new Random();

        // Création du graphe pondéré dirigé avec JGraphT
        SimpleDirectedWeightedGraph<String, DefaultWeightedEdge> graph = new SimpleDirectedWeightedGraph<>(DefaultWeightedEdge.class);

        // Demande du nombre de sommets
        System.out.print("Entrez le nombre de sommets : ");
        int numVertices = scanner.nextInt();
        scanner.nextLine(); // Consommer le retour à la ligne

        // Génération des sommets nommés x0 à xN
        String[] vertices = new String[numVertices];
        for (int i = 0; i < numVertices; i++) {
            vertices[i] = "x" + i;
            graph.addVertex(vertices[i]);
        }

        // Ajout des arêtes dirigées avec des poids aléatoires entre 1 et 100
        System.out.println("Ajout des arcs dirigés avec des pondérations aléatoires entre 1 et 100:");
        for (int i = 0; i < numVertices; i++) {
            for (int j = i + 1; j < numVertices; j++) {
                int weight = random.nextInt(100) + 1;
                DefaultWeightedEdge edge = graph.addEdge(vertices[i], vertices[j]);
                graph.setEdgeWeight(edge, weight);
                System.out.println(vertices[i] + " -> " + vertices[j] + " : " + weight);
            }
        }

        // Création du graphe GraphStream pour l'affichage
        Graph gsGraph = new SingleGraph("Graphe Dijkstra Dirigé");

        // Ajout des noeuds et arcs dans GraphStream
        for (String vertex : vertices) {
            gsGraph.addNode(vertex).setAttribute("ui.label", vertex); // Ajout des étiquettes pour les noeuds
        }

        for (DefaultWeightedEdge edge : graph.edgeSet()) {
            String source = graph.getEdgeSource(edge);
            String target = graph.getEdgeTarget(edge);
            double weight = graph.getEdgeWeight(edge);

            // Ajout de l'arc dans GraphStream avec les poids
            Edge gsEdge = gsGraph.addEdge(source + "->" + target, source, target, true); // true for directed edge
            gsEdge.setAttribute("ui.label", String.valueOf(weight)); // Conversion en chaîne de caractères
            gsEdge.setAttribute("weight", weight);
        }

        // Configuration de l'affichage
        gsGraph.display();

        // Demande des sommets de départ et d'arrivée pour Dijkstra
        System.out.print("Entrez le sommet de départ pour l'algorithme de bellman (ex: x0) : ");
        String startVertex = scanner.nextLine();
        System.out.print("Entrez le sommet d'arrivée pour l'algorithme de belman(ex: x1) : ");
        String endVertex = scanner.nextLine();

        // Vérifie si les sommets existent dans le graphe
        if (graph.containsVertex(startVertex) && graph.containsVertex(endVertex)) {
            // Calcul du plus court chemin avec Dijkstra
            DijkstraShortestPath<String, DefaultWeightedEdge> dijkstraAlg = new DijkstraShortestPath<>(graph);
            GraphPath<String, DefaultWeightedEdge> path = dijkstraAlg.getPath(startVertex, endVertex);

            if (path != null) {
                System.out.println("Distance minimale de " + startVertex + " à " + endVertex + " : " + path.getWeight());
                System.out.println("Chemin le plus court : " + path.getVertexList());

                // Coloration du chemin le plus court
                for (String vertex : path.getVertexList()) {
                    gsGraph.getNode(vertex).setAttribute("ui.style", "fill-color: red;"); // Coloration des noeuds en rouge
                }
                for (DefaultWeightedEdge edge : path.getEdgeList()) {
                    String source = graph.getEdgeSource(edge);
                    String target = graph.getEdgeTarget(edge);
                    gsGraph.getEdge(source + "->" + target).setAttribute("ui.style", "fill-color: blue; size: 3px;"); // Coloration des arcs en bleu
                }
            } else {
                System.out.println("Aucun chemin entre " + startVertex + " et " + endVertex);
            }
        } else {
            System.out.println("L'un des sommets n'existe pas dans le graphe.");
        }
    }
}
