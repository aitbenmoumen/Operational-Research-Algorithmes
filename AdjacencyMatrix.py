import random
import numpy  # type: ignore


def adjacencyMatrix():
    print("Type how much nodes are in your graph :")
    nodes = int(input())
    print("How many arcs :")
    arcs = int(input())
    counter = 0
    matrix = numpy.zeros((nodes,nodes))
    deg = numpy.zeros((nodes,2))

    
    # adding arcs 
    while(counter < arcs):
        i = random.randint(0,nodes-1)
        j = random.randint(0,nodes-1)
        if matrix[i][j] == 0 :
            matrix[i][j] = 1
            counter+=1

    # caluculate deg
    for i in range(nodes):
        degP = 0
        degM = 0
        for j in range(nodes):
            if matrix[i][j] == 1:
                degP+=1
            if matrix[j][i] == 1:
                degM+=1
        deg[i][0] = degP
        deg[i][1] = degM

    # Calculer le deg pour assurer le fait que le graph est oriente      
    sommeDP = 0
    sommeDM = 0
    for i in range(nodes):
        sommeDP+=deg[i][0]
    for i in range(nodes):
        sommeDM+=deg[i][1]
    
    
    # Display matrix
    for r in matrix:
        print(r)

    # Display the deg matrix
    for r in deg:
        print(r)
    print(f"la somme des degres+ vaut : {int(sommeDP)} et les degres- vaut {int(sommeDM)}")

    # Interpretation du graph
    for i in range(nodes):
        print("----------------------------------------")
        for j in range(nodes):
            if matrix[i][j] == 1:
                print(f"the node {i} is connected to the node {j}")

adjacencyMatrix()



    
