class Node:
    def __init__(self, name, x, y):
        self.name=name
        self.x=float(x)
        self.y=float(y)
        self.list_of_neighbors=[]

def AddNeighbor(n1,n2):
    if n2 in n1.list_of_neighbors:
        return False
    n1.list_of_neighbors.append(n2)
    return True
def distance(n1,n2):
    dx=n1.x-n2.x
    dy=n1.y-n2.y
    d=(dx**2+dy**2)**0.5
    return d
