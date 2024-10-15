/**
 * AdjacencyList
 */
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Random;

public class AdjacencyList {

    /**
     * InnerAdjacencyList
     */
    
    public static void main(String[] args) {
        Scanner scan = new Scanner(System.in);
        List<Integer> aList = new ArrayList<>();
        List<Integer> lList = new LinkedList<>();
        int nodes = 0, arcs = 0;
        Random random = new Random();

        System.out.print("Type how many nodes do you want in your graph :");
        nodes = scan.nextInt();
        System.out.println("How many arcs ? :");
        arcs = scan.nextInt();


        int counter = arcs;
        
        for(int i = 0; i < nodes; i++){
            aList.add(i);
            while (counter>arcs) {
                int x = random.nextInt(nodes+1);
                for(int k=0;k<x;k++){
                    lList.add(random.nextInt(nodes+1));
                }
                counter-=x;
            }
            counter=arcs;
        }

        for (Integer element : lList) {
                System.out.print(element + " ");
            }
            System.out.println();
        }
        
        
        
        








    }
}