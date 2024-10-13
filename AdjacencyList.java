/**
 * AdjacencyList
 */
import java.util.Scanner;
import java.util.List;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Random;

public class AdjacencyList {

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

        for(int i = 0;i < nodes; i++){
            aList.add(0,i);
        }
        for(int i = 0 ; i<aList.size() ; i++){
            for(int j = 0;j < random.nextInt(nodes);j++){

            }
        }

    }
}