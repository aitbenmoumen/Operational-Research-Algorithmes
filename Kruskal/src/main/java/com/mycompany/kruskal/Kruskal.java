/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.kruskal;
import java.util.Scanner;
import java.util.Random;
/**
 *
 * @author aaitb
 */
public class Kruskal {

    public static void main(String[] args) {
        Graph G = new Graph();
        Scanner sc = new Scanner(System.in);
        Random rd = new Random();
        System.out.println("Hello Friend !");
        System.out.print("enter the number of nodes :");
        
        int nodes = sc.nextInt();
        G.dimension(nodes); // fix the size of the initial linked list 
        System.out.print("enter the number of edges :");
        int edges = sc.nextInt();
        
        
        
        while (edges>(nodes*(nodes-1))/2){
            System.out.print("the number of edges must be lower or equal to "+ (nodes*(nodes-1))/2 +":");
            edges = sc.nextInt();
        }
        int s, w;
        // Random graph generation
        for (int i = 0; i < edges; i++) {
            s = rd.nextInt(nodes); // random source
            w = rd.nextInt(50); // random weight
            // I added nodes to generate destination and limit the random number to nodes
            G.add_Edge(s, w, nodes);
            
        }
        G.showGraph();
    }
}
