import numpy as np

def Initialize(n, m, aCost):
    # Initialize matrices
    aRoute = [[0] * m for _ in range(n)]
    aDual = [[-1] * m for _ in range(n)]
    return aRoute, aDual

def NorthWest(n, m, aRoute, aDemand, aSupply):
    # Initial feasible solution using North-West Corner Rule
    u, v = 0, 0
    while u < n and v < m:
        allocation = min(aDemand[v], aSupply[u])
        aRoute[u][v] = allocation
        aDemand[v] -= allocation
        aSupply[u] -= allocation
        if aSupply[u] == 0:
            u += 1
        if aDemand[v] == 0:
            v += 1

def FindPath(pivot_n, pivot_m, n, m, aRoute):
    # Initialize path with the pivot
    path = [(pivot_n, pivot_m)]
    
    # Find path by alternating between rows and columns
    def find_in_row(row, exclude_col):
        for col in range(m):
            if col != exclude_col and aRoute[row][col] > 0:
                return col
        return None

    def find_in_column(col, exclude_row):
        for row in range(n):
            if row != exclude_row and aRoute[row][col] > 0:
                return row
        return None

    while True:
        last_row, last_col = path[-1]

        # Alternate between finding in column and row
        if len(path) % 2 == 1:  # Odd: Look in column
            next_row = find_in_column(last_col, last_row)
            if next_row is None:
                break
            path.append((next_row, last_col))
        else:  # Even: Look in row
            next_col = find_in_row(last_row, last_col)
            if next_col is None:
                break
            path.append((last_row, next_col))
        
        # Stop if loop is closed
        if path[-1] == path[0]:
            break

    return path

def NotOptimal(n, m, aDual):
    # Check if current solution is optimal
    nMax = -np.inf
    pivot_n, pivot_m = -1, -1
    for u in range(n):
        for v in range(m):
            x = aDual[u][v]
            if x > nMax:
                nMax = x
                pivot_n, pivot_m = u, v
    return nMax > 0, pivot_n, pivot_m

def BetterOptimal(aRoute, aPath):
    # Improve solution by pivoting on the most profitable arc
    nMin = np.inf
    for w in range(1, len(aPath), 2):
        t = aRoute[aPath[w][0]][aPath[w][1]]
        nMin = min(nMin, t)
    for w in range(len(aPath)):
        u, v = aPath[w]
        aRoute[u][v] += nMin if w % 2 == 0 else -nMin

def PrintOut(n, m, aRoute, aCost):
    # Print current solution and its cost
    print("Route:")
    for u in range(n):
        print(f"Source {u+1}:")
        for v in range(m):
            print(f"  {aRoute[u][v]:4} -> {v+1}")
    total_cost = sum(aRoute[i][j] * aCost[i][j] for i in range(n) for j in range(m))
    print(f"Cost: {total_cost}")

# Example
print("Saisir le nombre des usines")
lines = int(input())
print("Saisir le nombre des magasins")
cols = int(input())

aCost = np.random.randint(0,30,size=(lines,cols))
aDemand = [30, 50, 20, 40, 25, 15]
aSupply = [50, 40, 60, 31]

# Initialize and run the algorithm
aRoute, aDual = Initialize(n, m, aCost)
NorthWest(n, m, aRoute, aDemand, aSupply)

while True:
    optimal, pivot_n, pivot_m = NotOptimal(n, m, aDual)
    if not optimal:
        break
    aPath = FindPath(pivot_n, pivot_m, n, m, aRoute)
    BetterOptimal(aRoute, aPath)
    PrintOut(n, m, aRoute, aCost)

print("FINISHED")
