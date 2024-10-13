import java.util.Random;
import java.util.Scanner;

public class AdjacencyMatrix {
    public static void calculerDeg(int n, int[][] matrice) {

        int[][] deg = new int[n][2];
        int sommeP = 0, sommeM = 0;
        for (int i = 0; i < n; i++) {
            int degP = 0, degM = 0;
            for (int j = 0; j < n; j++) {
                if (matrice[i][j] == 1) {
                    degP++;
                }
                if (matrice[j][i] == 1) {
                    degM++;
                }
            }
            deg[i][0] = degP;
            deg[i][1] = degM;
        }
        System.out.println("-------Matrice Deg-------");
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < 2; j++) {
                System.out.print(" " + deg[i][j] + " ");
            }
            System.out.println();
        }
        for (int i = 0; i < n; i++) {
            sommeP += deg[i][0];
            sommeM += deg[i][1];
        }
        System.out.println(
                "Somme de Deg+ = " + sommeP + " et Deg- = " + sommeM + "\n--------------------------------------");
    }

    public static void main(String[] args) {

        Random random = new Random();
        Scanner scan = new Scanner(System.in);
        int n, arc, i, j, counter = 0;

        System.out.print("Type the number of nodes :");
        n = scan.nextInt();
        // forçage des arcs
        while (true) {
            System.out.print("Type the number of arcs :");
            arc = scan.nextInt();
            if (arc < Math.pow(n, 2)) {
                break;
            }
        }

        // pour la matrice
        int[][] matrice = new int[n][n];
        // pour calculer les deg+ et deg- afin d'assurer que le graphe est oriente

        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                matrice[i][j] = 0;
            }
        }

        // pour assurer le nb des arcs via un compteur qui compte le nombre des 1 dans
        // la matrice
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

        // pour calculer et remplir la matrice deg
        calculerDeg(n, matrice);

        // traduire les arcs
        for (i = 0; i < n; i++) {
            for (j = 0; j < n; j++) {
                if (matrice[i][j] == 1) {
                    System.out.println("Node " + i + " is connected to " + j);
                }
            }
            System.out.println("--------------------------------------");
            System.out.println();
        }

    }
}
