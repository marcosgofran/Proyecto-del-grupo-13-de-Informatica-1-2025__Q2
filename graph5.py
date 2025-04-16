from node1 import Node, AddNeighbor, distance
from segment3 import Segment
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.nodes = []
        self.segments = []


def AddNode(g, n):
    for node in g.nodes:
        if node.name == n.name:
            return False
    g.nodes.append(n)
    return True


def AddSegment(g, name, nameOriginNode, nameDestinationNode):
    origin = None
    destination = None
    for node in g.nodes:
        if node.name == nameOriginNode:
            origin = node
        if node.name == nameDestinationNode:
            destination = node
    if origin is None or destination is None:
        return False
    s = Segment(name, origin, destination)
    g.segments.append(s)

    # ✅ Línea clave añadida para que ReachableNodes funcione correctamente
    if destination not in origin.list_of_neighbors:
        origin.list_of_neighbors.append(destination)

    return True


def GetClosest(g, x, y):
    closest = None
    min_dist = None
    for node in g.nodes:
        d = ((node.x - x)**2 + (node.y - y)**2)**0.5
        if closest is None or d < min_dist:
            closest = node
            min_dist = d
    return closest


def Plot(g):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.set_title("Grafo")
    ax.axis("equal")
    ax.grid(True)

    # Dibujar segmentos
    for seg in g.segments:
        x1, y1 = seg.origin.x, seg.origin.y
        x2, y2 = seg.destination.x, seg.destination.y
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.annotate("",
                    xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black"))
        ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8)

    # Dibujar nodos
    for node in g.nodes:
        ax.plot(node.x, node.y, "o", color="gray")
        ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=9)

    return fig, ax



def PlotNode(g, nameOrigin):
    origin = None
    for node in g.nodes:
        if node.name == nameOrigin:
            origin = node
            break
    if origin is None:
        return False

    plt.figure()
    for node in g.nodes:
        if node == origin:
            plt.plot(node.x, node.y, "o", color="blue")
        elif node in origin.list_of_neighbors:
            plt.plot(node.x, node.y, "o", color="green")
        else:
            plt.plot(node.x, node.y, "o", color="gray")
        plt.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=9)

    for seg in g.segments:
        if seg.origin == origin and seg.destination in origin.list_of_neighbors:
            x1, y1 = seg.origin.x, seg.origin.y
            x2, y2 = seg.destination.x, seg.destination.y
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.annotate("",
                        xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color=color, lw=1.5))

            plt.text(mx, my, f"{seg.cost:.1f}", fontsize=7, color="red")

    plt.title(f"Neighborhood of node {nameOrigin}")
    plt.grid(True)
    plt.axis("equal")
    plt.show()
    return True

def CreateGraphFromFile(filename):
    g = Graph()
    with open(filename, 'r') as f:
        lines = f.readlines()

    mode = None  # Puede ser "nodes" o "segments"

    for line in lines:
        line = line.strip()

        if line == "":
            continue
        elif "# NODES" in line:
            mode = "nodes"
            continue
        elif "# SEGMENTS" in line:
            mode = "segments"
            continue

        if mode == "nodes":
            name, x, y = line.split()
            AddNode(g, Node(name, float(x), float(y)))
        elif mode == "segments":
            seg_name, origin, destination = line.split()
            AddSegment(g, seg_name, origin, destination)

    return g



def CreateGraph_1 ():
 G = Graph()
 AddNode(G, Node("A",1,20))
 AddNode(G, Node("B",8,17))
 AddNode(G, Node("C",15,20))
 AddNode(G, Node("D",18,15))
 AddNode(G, Node("E",2,4))
 AddNode(G, Node("F",6,5))
 AddNode(G, Node("G",12,12))
 AddNode(G, Node("H",10,3))
 AddNode(G, Node("I",19,1))
 AddNode(G, Node("J",13,5))
 AddNode(G, Node("K",3,15))
 AddNode(G, Node("L",4,10))
 AddSegment(G, "AB","A","B")
 AddSegment(G, "AE","A","E")
 AddSegment(G, "AK","A","K")
 AddSegment(G, "BA","B","A")
 AddSegment(G, "BC","B","C")
 AddSegment(G, "BF","B","F")
 AddSegment(G, "BK","B","K")
 AddSegment(G, "BG","B","G")
 AddSegment(G, "CD","C","D")
 AddSegment(G, "CG","C","G")
 AddSegment(G, "DG","D","G")
 AddSegment(G, "DH","D","H")
 AddSegment(G, "DI","D","I")
 AddSegment(G, "EF","E","F")
 AddSegment(G, "FL","F","L")
 AddSegment(G, "GB","G","B")
 AddSegment(G, "GF","G","F")
 AddSegment(G, "GH","G","H")
 AddSegment(G, "ID","I","D")
 AddSegment(G, "IJ","I","J")
 AddSegment(G, "JI","J","I")
 AddSegment(G, "KA","K","A")
 AddSegment(G, "KL","K","L")
 AddSegment(G, "LK","L","K")
 AddSegment(G, "LF","L","F")
 return G


def CreateGraph_2():
    G = Graph()
    AddNode(G, Node("X", 0, 0))
    AddNode(G, Node("Y", 5, 5))
    AddNode(G, Node("Z", 10, 0))
    AddNode(G, Node("W", 5, -5))

    AddSegment(G, "XY", "X", "Y")
    AddSegment(G, "YZ", "Y", "Z")
    AddSegment(G, "ZW", "Z", "W")
    AddSegment(G, "WX", "W", "X")
    AddSegment(G, "XW", "X", "W")

    return G



