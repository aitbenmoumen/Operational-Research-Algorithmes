/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.implementation_graph_aleatoire;
import java.util.*;
import org.graphstream.graph.Edge;
import org.graphstream.graph.Graph;
import org.graphstream.graph.implementations.SingleGraph;
import org.jgrapht.alg.shortestpath.DijkstraShortestPath;
import org.jgrapht.graph.DefaultWeightedEdge;
import org.jgrapht.graph.SimpleDirectedWeightedGraph;
import org.jgrapht.GraphPath;
/**
 *
 * @author aaitb
 */
public class Implementation_Graph_Aleatoire {

    public static void main(String[] args) {
        System.out.println("Hello friend !!");
        Scanner scan = new Scanner(System.in);
        Random rand = new Random();
        System.out.println("Saisir le nombre de sommets : ");
        int vertices = scan.nextInt();
        SimpleDirectedWeightedGraph<String, DefaultWeightedEdge> graph = new SimpleDirectedWeightedGraph<>(DefaultWeightedEdge.class);
        String[] nodes = new String[vertices];
        
        // ajouter des noeuds au graphe
        for(int i = 0 ; i < vertices ; i++){
            nodes[i] = "x" + i;
            graph.addVertex(nodes[i]); // cette methode accepte que des string comme parametre 
        }
        
        
        // ajouter des arrets
        for(int i = 0; i < vertices ; i++){
            for(int j = i + 1 ; j < vertices ; j++){
                DefaultWeightedEdge edge = graph.addEdge(nodes[i], nodes[j]); // store the edge in a variable in order to reuse when you want to set 
                int weight = rand.nextInt(0,100);                                                              // the edge weight 
                graph.setEdgeWeight(edge, weight);
                System.out.println(nodes[i]+"-->"+nodes[j]+" : "+ weight);
            }
        }
        
        // Création du graphe GraphStream pour l'affichage
        Graph gsGraph = new SingleGraph("Random Directed Graph");
        
        // Ajout des noeuds et arcs dans GraphStream
        for (String vertex : nodes) {
            gsGraph.addNode(vertex).setAttribute("ui.label", vertex); // Ajout des étiquettes pour les noeuds
        }
        
        // ajout des arrets 
        for(DefaultWeightedEdge edge : graph.edgeSet()){
            String source = graph.getEdgeSource(edge);
            String destination = graph.getEdgeTarget(edge);
            double weight = graph.getEdgeWeight(edge);
            
            Edge gsEdge = gsGraph.addEdge(source+" -> "+destination, source, destination, true);
            gsEdge.setAttribute("weight", weight);
            gsEdge.setAttribute("ui.label", String.valueOf(weight)); // set lables 3la 9bl l weight dial l edges  
            
        }
        gsGraph.display();
    }
}
