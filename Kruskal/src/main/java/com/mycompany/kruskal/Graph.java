/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kruskal;

import java.util.LinkedList;
import java.util.Random;
import java.util.Scanner;

/**
 *
 * @author aaitb
 */

public class Graph {
    private LinkedList<Node> adjacency[];
    
    public void dimension(int d){
        adjacency = new LinkedList[d];
        for(int i=0;i<d;i++){
            adjacency[i] = new LinkedList<Node>();
        }
    }
    // add the edges
    public void add_Edge(int s, int w,int nodes) {
    Random rd = new Random();
    int d;

    while (true) {
        d = rd.nextInt(nodes);
        while (s == d) {
            d = rd.nextInt(nodes);
        }
        // Check for duplicates in the source node's adjacency list
        boolean existsInSource = false;
        for (Node node : adjacency[s]) {
            if (node.getVerticle() == d) {
                existsInSource = true;
                break;
            }
        }

        // If no duplicate found, add the edge
        if (!existsInSource) {
            Node newNode = new Node(d, w);
            adjacency[s].add(newNode);

            // Add reverse edge for undirected graph
            boolean existsInDest = false;
            for (Node node : adjacency[d]) {
                if (node.getVerticle() == s) {
                    existsInDest = true;
                    break;
                }
            }
            if (!existsInDest) {
                Node reverseNode = new Node(s, w);
                adjacency[d].add(reverseNode);
            }

            System.out.println("Edge added: " + s + " -> " + d + " with weight " + w);
            break; // Exit the loop after successfully adding the edge
        }
    }
}


    
    public void showGraph(){
        for(int i=0;i<adjacency.length;i++){
            System.err.print(i+" :");
            for(int j=0;j<adjacency[i].size();j++){
                System.err.print(adjacency[i].get(j).getVerticle()+" ("+adjacency[i].get(j).getWeight()+")");
                if(j<adjacency[i].size()-1){
                    System.err.print(" -> ");
                }
            }
            System.out.println("");
        }
    }
}
