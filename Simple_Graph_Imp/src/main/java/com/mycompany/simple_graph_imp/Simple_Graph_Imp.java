/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.simple_graph_imp;
import java.util.*;
/**
 *
 * @author aaitb
 */
public class Simple_Graph_Imp {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Graph g = new Graph();
        System.out.println("Hello Friend !");
        System.out.println("Type the number of verticles and edges :");
        int v = sc.nextInt();
        int e = sc.nextInt();
        
        g.add_verticles(v);
        
        for(int i = 0;i<e;i++){
            System.out.println("Enter the source and destination:");
            int s = sc.nextInt();
            int d = sc.nextInt();
            if (s < 0 || s >= v || d < 0 || d >= v) {
                System.out.println("Invalid vertex. Please enter vertices between 0 and " + (v - 1) + ".");
                i--; // decrementer i pour ne pas perdre l'enchainement 
                continue; // skip to the next iteration
            }
            g.add_edges(s, d);
        }
        g.show_graph(v);
        sc.close();
    }
}
