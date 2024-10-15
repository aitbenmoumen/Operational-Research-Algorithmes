import random
import numpy 


def adjacencyMatrix():
    print("Type how much nodes are in your graph :")
    nodes = int(input())
    print("How many arcs :")
    arcs = int(input())
    counter = 0
    matrix = [[0 for _ in range(nodes)]for _ in range(nodes)]
    deg = numpy.zeros((nodes,2))
    
    # filling the matrix with 0's 
    for i in range(nodes):
        for j in range(nodes):
            matrix[i][j] = 0
    
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


    # Display matrix
    for r in matrix:
        print(r)

    # Display the deg matrix
    for r in deg:
        print(r)


    # Interpretation du graph
    for i in range(nodes):
        print("----------------------------------------")
        for j in range(nodes):
            if matrix[i][j] == 1:
                print(f"the node {i} is connected to the node {j}")

adjacencyMatrix()



    
