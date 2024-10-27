/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.mycompany.kruskal;

/**
 *
 * @author aaitb
 */
public class Node {
    private int verticle;
    private int weight;
    public Node(int v,int w){
        this.verticle = v;
        this.weight = w;
    }
    public int getVerticle(){
        return this.verticle;
    }
    public void setVerticle(int v){
        this.verticle = v;
    }
    public int getWeight(){
        return this.weight;
    }
    public void setWeight(int w){
        this.weight = w;
    }
}
