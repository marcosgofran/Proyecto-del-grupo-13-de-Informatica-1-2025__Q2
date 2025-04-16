from segment3 import *
from node1 import *   # si usas nodos dentro


n1 = Node('A', 0, 0)
n2 = Node('B', 3, 4)
n3 = Node('C', 6, 0)

s1 = Segment('S1', n1, n2)
s2 = Segment('S2', n2, n3)

print(f"Segment {s1.name}: from {s1.origin.name} to {s1.destination.name}, cost = {s1.cost}")
print(f"Segment {s2.name}: from {s2.origin.name} to {s2.destination.name}, cost = {s2.cost}")
