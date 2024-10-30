/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 */

package com.mycompany.djikstra;
import java.util.ArrayList;
/**
 *
 * @author aaitb
 */



public class Djikstra {

    public static void main(String[] args) {
        
        Graph G = new Graph(4);
        G.random_graph(4, 8);
        G.display();
        
        
    }
}
