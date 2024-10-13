import random

def adjacencyMatrix():
    print("Type how much nodes are in your graph :")
    nodes = int(input())
    print("How many arcs :")
    arcs = int(input())
    counter = 0
    matrix = [[0 for _ in range(nodes)]for _ in range(nodes)]
    
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
    
    # Display matrix
    for r in matrix:
        print(r)

    # Interpretation du graph
    for i in range(nodes):
        print("----------------------------------------")
        for j in range(nodes):
            if matrix[i][j] == 1:
                print(f"the node {i} is connected to the node {j}")

adjacencyMatrix()



    
