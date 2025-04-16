from path10 import Path, AddNodeToPath, ContainsNode, CostToNode, PlotPath
from node1 import Node
from graph5 import Graph, AddNode, AddSegment

# Crear algunos nodos y segmentos
n1 = Node("A", 0, 0)
n2 = Node("B", 3, 4)
n3 = Node("C", 6, 0)

# Crear un grafo de prueba
G = Graph()
AddNode(G, n1)
AddNode(G, n2)
AddNode(G, n3)
AddSegment(G, "S1", "A", "B")
AddSegment(G, "S2", "B", "C")

# Crear un camino vacío
p = Path()
print("Camino vacío:", p)

# Añadir nodos al camino
AddNodeToPath(p, n1, 0)         # nodo inicial, coste 0
AddNodeToPath(p, n2, 5.0)       # A → B, distancia 5
AddNodeToPath(p, n3, 5.0)       # B → C, distancia 5
print("Camino con nodos:", p)

# Probar ContainsNode
print("¿Contiene B?", ContainsNode(p, n2))  # True
print("¿Contiene nodo ficticio?", ContainsNode(p, Node("X", 1, 1)))  # False

# Probar CostToNode
print("Coste hasta B:", CostToNode(p, n2))  # Debe ser parcial
print("Coste hasta C:", CostToNode(p, n3))  # Total
print("Coste hasta nodo no existente:", CostToNode(p, Node("X", 0, 0)))  # -1

# Dibujar camino sobre el grafo
PlotPath(G, p)


from path10 import ReachableNodes, FindShortestPath
from graph5 import CreateGraph_1

print("\n== TEST ReachableNodes ==")
G2 = CreateGraph_1()
alcanzables = ReachableNodes(G2, "A")
print("Desde A se puede llegar a:", [n.name for n in alcanzables])

print("\n== TEST FindShortestPath (A -> F) ==")
camino = FindShortestPath(G2, "A", "F")
if camino:
    print("Camino más corto de A a F:", camino)
else:
    print("No hay camino de A a F.")


from graph5 import CreateGraph_1
from path10 import ReachableNodes

g = CreateGraph_1()
alcanzables = ReachableNodes(g, "B")
print("Desde B se puede alcanzar a:", [n.name for n in alcanzables])


from graph5 import CreateGraph_1
from path10 import ReachableNodes

g = CreateGraph_1()
alcanzables = ReachableNodes(g, "B")
print("Desde B se puede alcanzar:", [n.name for n in alcanzables])
