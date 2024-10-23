/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.simple_graph_imp;
import java.util.*;
/**
 *
 * @author aaitb
 */
public class Graph {
    // declaration
    private LinkedList<Integer> adjacency[];
    // reservation et initialisation
    public void add_verticles(int v){
        adjacency = new LinkedList[v];
        for(int i = 0;i < v; i++){
            adjacency[i] = new LinkedList<Integer>();
        }
    }
    // etablissement des liens 
    public void add_edges(int s, int d){
        adjacency[s].add(d);
        adjacency[d].add(s);   
    }
    // afficher le graphe 
    public void show_graph(int v){
        for(int i = 0;i < adjacency.length;i++){
            System.out.print(i+" : ");
            for(int j = 0;j<adjacency[i].size();j++){
                System.out.print(adjacency[i].get(j));
                if(j < adjacency[i].size()-1 ){
                    System.out.print(" -> ");
                }
            }
            System.out.println("");
        }
    }
}
