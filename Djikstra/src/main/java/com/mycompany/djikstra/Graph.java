/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.djikstra;


import java.util.ArrayList;
import java.util.Random;

/**
 *
 * @author aaitb
 */
public class Graph {
    
    private int[][] matrix;
    public Graph(int verticles){
        this.matrix = new int[verticles][verticles];
        for(int i=0;i<verticles;i++){
            for(int j=0;j<verticles;j++){
                matrix[i][j]=0;
            }
        }
    }
    public void random_graph(int verticles,int edges){
        if(edges <= Math.pow(verticles, 2)){
        Random rand = new Random();
        int i,j,count=edges;
        while(count>0){
            i = rand.nextInt(verticles);
            j = rand.nextInt(verticles);
            if(matrix[i][j] == 0){
                matrix[i][j] = rand.nextInt(100);
                count--;
            }
        }
        }else{
            System.err.println("The maximum number of edges for your graph is "+Math.pow(verticles, 2));
        }
    }
    public void display() {
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                System.err.print(matrix[i][j] + "\t");
            }
            System.err.println();
        }
    }
    public void djikstra(int racine){
        int count;
        ArrayList<Integer> u = new ArrayList<>();
        ArrayList<Integer> du = new ArrayList<>();
        ArrayList<Integer> parent = new ArrayList<>();
        ArrayList<Integer> f = new ArrayList<>();
        
        for(int i=0;i<4;i++){
            u.add(i);
            du.add(Integer.MAX_VALUE);
            parent.add(null);
            f.add(i);
        }
        
        while(!f.isEmpty()){
            count=0;
            du.add(racine, 0);
            f.remove(racine);
            for(int i=0;i<matrix[racine].length;i++){
                if(matrix[racine][i]!= 0){
                    count++;
                    // d[v] = du[racine]+w(u,v) si d[v]>du[racine]+w(u,v)
                    if(matrix[racine][i]>du.get(racine)){
                        matrix[racine][i] = du.get(racine)+0;// just a temporary thing 
                    }
                }
            }
        }
    }
}

