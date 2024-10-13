import java.util.Random;
import java.util.Scanner;

public class AdjacencyMatrix {
    public static void main(String[] args) {

        Random random = new Random();
        Scanner scan = new Scanner(System.in);
        int n, arc, i, j, counter = 0;

        System.out.print("Type the number of nodes :");
        n = scan.nextInt();
        System.out.print("Type the number of arcs :");
        arc = scan.nextInt();

        int[][] matrice = new int[n][n];
        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                matrice[i][j] = 0;
            }
        }

        // pour assurer le nb des arcs via un compteur qui compte le nombre des 1 dans la matrice
        while (counter < arc) {
            i = random.nextInt(n);
            j = random.nextInt(n);
            if (matrice[i][j] == 0) {
                matrice[i][j] = 1;
                counter++;
            }
        }

        // afficher la matrice 
        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                System.out.print(" " + matrice[i][j] + " ");
            }
            System.out.println();
        }
        
        // traduire les arcs
        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                if(matrice[i][j]==1){
                    System.out.println("Node "+i+" is connected to "+j);
                }
            }
            System.out.println("--------------------------------------");
            System.out.println();
        }

    }
}
