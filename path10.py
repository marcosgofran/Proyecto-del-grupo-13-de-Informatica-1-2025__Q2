from node1 import distance

class Path:
    def __init__(self):
        self.nodes = []  # lista de nodos en el camino
        self.cost = 0.0  # coste total del camino (que es la distancia)

    def __repr__(self):
        return " -> ".join([n.name for n in self.nodes]) + f" (cost: {self.cost:.2f})"
def AddNodeToPath(p, n, segment_cost):
    p.nodes.append(n)
    p.cost += segment_cost
    return p

def ContainsNode(p, n):
    return n in p.nodes

def CostToNode(p, n):
    if n in p.nodes:
        index = p.nodes.index(n)
        partial_nodes = p.nodes[:index+1]
        return (index / (len(p.nodes)-1)) * p.cost if len(p.nodes) > 1 else 0.0
    return -1

def PlotPath(g, path):
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    ax.set_title("Camino más corto")
    ax.axis("equal")
    ax.grid(True)

    # 1. Dibujar todos los segmentos en negro
    for seg in g.segments:
        x1, y1 = seg.origin.x, seg.origin.y
        x2, y2 = seg.destination.x, seg.destination.y
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black"))
        ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8)

    # 2. Dibujar todos los nodos en gris
    for node in g.nodes:
        ax.plot(node.x, node.y, "o", color="gray")
        ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=9)

    # 3. Dibujar el camino más corto en azul
    for i in range(len(path.nodes) - 1):
        n1 = path.nodes[i]
        n2 = path.nodes[i + 1]
        ax.annotate("", xy=(n2.x, n2.y), xytext=(n1.x, n1.y),
                    arrowprops=dict(arrowstyle="->", color="blue", lw=2))

    # 👇 MUY IMPORTANTE: devolvemos la figura
    return fig


def FindShortestPath(graph, origin_name, destination_name):
    from queue import PriorityQueue
    origin = next((n for n in graph.nodes if n.name == origin_name), None)
    destination = next((n for n in graph.nodes if n.name == destination_name), None)

    if not origin or not destination:
        return None

    frontier = PriorityQueue()
    frontier.put((0, origin))
    came_from = {origin: None}
    cost_so_far = {origin: 0}

    while not frontier.empty():
        current_cost, current_node = frontier.get()

        if current_node == destination:
            break

        for neighbor in current_node.list_of_neighbors:
            segment = next((s for s in graph.segments if s.origin == current_node and s.destination == neighbor), None)
            if segment is None:
                continue

            new_cost = cost_so_far[current_node] + segment.cost
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                frontier.put((new_cost, neighbor))
                came_from[neighbor] = current_node

    if destination not in came_from:
        return None

    # reconstruir camino como objeto Path
    from path10 import Path, AddNodeToPath
    path = Path()
    current = destination
    steps = []
    while current:
        steps.append(current)
        current = came_from[current]
    steps.reverse()

    for i in range(len(steps) - 1):
        n1, n2 = steps[i], steps[i + 1]
        segment = next((s for s in graph.segments if s.origin == n1 and s.destination == n2), None)
        if segment:
            AddNodeToPath(path, n1, segment.cost)
    AddNodeToPath(path, steps[-1], 0)
    return path



def ReachableNodes(graph, origin_name):
    origin = next((n for n in graph.nodes if n.name == origin_name), None)
    if not origin:
        return []

    visited = set()
    queue = [origin]

    while queue:
        current = queue.pop(0)
        if current not in visited:
            visited.add(current)
            for neighbor in current.list_of_neighbors:
                if neighbor not in visited and neighbor not in queue:
                    queue.append(neighbor)

    visited.discard(origin)  # para no incluir el origen como alcanzable
    return list(visited)



from node1 import distance

def FindShortestPath(graph, origin_name, destination_name):
    origin = next((n for n in graph.nodes if n.name == origin_name), None)
    destination = next((n for n in graph.nodes if n.name == destination_name), None)

    if origin is None or destination is None:
        return None

    current_paths = []

    # Crear el primer camino con solo el nodo origen
    initial_path = Path()
    AddNodeToPath(initial_path, origin, 0.0)
    current_paths.append(initial_path)

    while current_paths:
        # Buscar el camino con el menor coste estimado (real + heurístico)
        best_index = 0
        best_cost = current_paths[0].cost + distance(current_paths[0].nodes[-1], destination)
        for i in range(1, len(current_paths)):
            total_cost = current_paths[i].cost + distance(current_paths[i].nodes[-1], destination)
            if total_cost < best_cost:
                best_index = i
                best_cost = total_cost

        path = current_paths.pop(best_index)
        last_node = path.nodes[-1]

        # Si hemos llegado al destino, devolvemos el camino
        if last_node == destination:
            return path

        # Expandir el camino con todos los vecinos del último nodo
        for neighbor in last_node.list_of_neighbors:
            if ContainsNode(path, neighbor):
                continue  # Evitar ciclos

            # Ver si ya hay otro camino que llega a ese nodo con menor coste
            new_cost = path.cost + distance(last_node, neighbor)
            worse_path_exists = False
            for other in current_paths:
                if other.nodes[-1] == neighbor and other.cost <= new_cost:
                    worse_path_exists = True
                    break
            if worse_path_exists:
                continue

            # Crear nuevo camino
            new_path = Path()
            new_path.nodes = list(path.nodes)
            new_path.cost = path.cost
            AddNodeToPath(new_path, neighbor, distance(last_node, neighbor))
            current_paths.append(new_path)

    return None  # No hay camino posible
