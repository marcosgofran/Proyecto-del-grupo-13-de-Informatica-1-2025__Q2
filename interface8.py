import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from graph5 import *
from node1 import Node
from path10 import PlotPath, FindShortestPath, ReachableNodes


root = tk.Tk()
root.title("Grafo Aéreo - Versión 2")
root.geometry("1000x700")

# Crear frames
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Variables globales
current_graph = Graph()
current_canvas = None
click_add_node_mode = False
click_delete_node_mode = False
click_delete_segment_mode = False
pending_node_name = None


# Funciones principales

def draw_graph():
    global current_canvas
    fig, ax = plt.subplots()
    ax.set_title("Grafo actual")
    ax.axis("equal")
    ax.grid(True)

    # Dibujar segmentos con flechas y mostrar solo coste
    for seg in current_graph.segments:
        x1, y1 = seg.origin.x, seg.origin.y
        x2, y2 = seg.destination.x, seg.destination.y
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.annotate("",
                    xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
        ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8, color="black")

    # Dibujar nodos
    for node in current_graph.nodes:
        ax.plot(node.x, node.y, "o", color="gray")
        ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=9)

    # Eliminar canvas anterior
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.mpl_connect("button_press_event", on_graph_click)
    globals()['current_canvas'] = canvas


def on_graph_click(event):
    global click_add_node_mode, click_delete_node_mode, click_delete_segment_mode, pending_node_name

    if event.xdata is None or event.ydata is None:
        return

    x, y = event.xdata, event.ydata

    if click_add_node_mode:
        new_node = Node(pending_node_name, x, y)
        success = AddNode(current_graph, new_node)
        if success:
            messagebox.showinfo("Nodo añadido", f"Se añadió el nodo '{pending_node_name}'.", parent=root)
        else:
            messagebox.showwarning("Duplicado", f"Ya existe un nodo con el nombre '{pending_node_name}'.", parent=root)
        click_add_node_mode = False
        draw_graph()
        return

    if click_delete_node_mode:
        closest = GetClosest(current_graph, x, y)
        if closest:
            current_graph.nodes.remove(closest)
            current_graph.segments = [s for s in current_graph.segments if s.origin != closest and s.destination != closest]
            for n in current_graph.nodes:
                if closest in n.list_of_neighbors:
                    n.list_of_neighbors.remove(closest)
            messagebox.showinfo("Nodo eliminado", f"Se eliminó el nodo '{closest.name}'.", parent=root)
            click_delete_node_mode = False
            draw_graph()
        return

    if click_delete_segment_mode:
        clicked_segment = None
        threshold = 0.3
        for seg in current_graph.segments:
            x1, y1 = seg.origin.x, seg.origin.y
            x2, y2 = seg.destination.x, seg.destination.y
            dx = x2 - x1
            dy = y2 - y1
            if dx == dy == 0:
                continue
            t = ((x - x1) * dx + (y - y1) * dy) / (dx**2 + dy**2)
            t = max(0, min(1, t))
            nearest_x = x1 + t * dx
            nearest_y = y1 + t * dy
            dist = ((x - nearest_x)**2 + (y - nearest_y)**2)**0.5
            if dist < threshold:
                clicked_segment = seg
                break
        if clicked_segment:
            current_graph.segments.remove(clicked_segment)
            if clicked_segment.destination in clicked_segment.origin.list_of_neighbors:
                clicked_segment.origin.list_of_neighbors.remove(clicked_segment.destination)
            messagebox.showinfo("Segmento eliminado", f"Se eliminó el segmento de {clicked_segment.origin.name} a {clicked_segment.destination.name}.", parent=root)
        click_delete_segment_mode = False
        draw_graph()


# Funciones por botón

def create_empty_graph():
    global current_graph
    current_graph = Graph()
    draw_graph()

def show_example_graph():
    global current_graph
    current_graph = CreateGraph_1()
    draw_graph()

def show_custom_graph():
    global current_graph
    current_graph = CreateGraph_2()
    draw_graph()

def load_graph_from_file():
    global current_graph
    filepath = filedialog.askopenfilename(
        title="Selecciona un archivo de grafo",
        filetypes=[("Text Files", "*.txt")],
        parent=root
    )
    if filepath:
        current_graph = CreateGraphFromFile(filepath)
        draw_graph()

def save_graph_to_file():
    filepath = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Guardar grafo como",
        parent=root
    )
    if not filepath:
        return
    try:
        with open(filepath, "w") as f:
            f.write("# NODES\n")
            for node in current_graph.nodes:
                f.write(f"{node.name} {node.x} {node.y}\n")
            f.write("\n# SEGMENTS\n")
            for seg in current_graph.segments:
                f.write(f"{seg.name} {seg.origin.name} {seg.destination.name}\n")
        messagebox.showinfo("Guardado", "Grafo guardado correctamente.", parent=root)
    except Exception as e:
        messagebox.showerror("Error", str(e), parent=root)

def add_node_click():
    global click_add_node_mode, pending_node_name
    name = simpledialog.askstring("Añadir nodo", "Introduce el nombre del nodo:", parent=root)
    if name:
        click_add_node_mode = True
        pending_node_name = name


def add_node_manual():
    name = simpledialog.askstring("Nombre del nodo", "Introduce el nombre del nodo:", parent=root)
    if not name:
        return
    try:
        x = float(simpledialog.askstring("X", "Coordenada X:", parent=root))
        y = float(simpledialog.askstring("Y", "Coordenada Y:", parent=root))
    except:
        messagebox.showerror("Error", "Coordenadas no válidas", parent=root)
        return
    success = AddNode(current_graph, Node(name, x, y))
    if success:
        messagebox.showinfo("Nodo añadido", f"Nodo '{name}' añadido correctamente.", parent=root)
    else:
        messagebox.showwarning("Duplicado", f"El nodo '{name}' ya existe.", parent=root)
    draw_graph()

def add_segment_manual():
    name = simpledialog.askstring("Nombre del segmento", "Introduce el nombre del segmento:", parent=root)
    origin = simpledialog.askstring("Origen", "Nombre del nodo origen:", parent=root)
    dest = simpledialog.askstring("Destino", "Nombre del nodo destino:", parent=root)
    if name and origin and dest:
        success = AddSegment(current_graph, name, origin, dest)
        if success:
            messagebox.showinfo("Segmento añadido", f"Segmento '{name}' añadido de {origin} a {dest}.", parent=root)
        else:
            messagebox.showerror("Error", "No se pudo añadir el segmento.", parent=root)
        draw_graph()

def delete_node_manual():
    name = simpledialog.askstring("Eliminar nodo", "Introduce el nombre del nodo:", parent=root)
    if not name:
        return
    node_to_remove = next((n for n in current_graph.nodes if n.name == name), None)
    if node_to_remove:
        current_graph.nodes.remove(node_to_remove)
        current_graph.segments = [s for s in current_graph.segments if s.origin != node_to_remove and s.destination != node_to_remove]
        for n in current_graph.nodes:
            if node_to_remove in n.list_of_neighbors:
                n.list_of_neighbors.remove(node_to_remove)
        messagebox.showinfo("Nodo eliminado", f"Nodo '{name}' eliminado.", parent=root)
        draw_graph()
    else:
        messagebox.showerror("Error", f"Nodo '{name}' no encontrado.", parent=root)

def delete_node_click():
    global click_delete_node_mode
    click_delete_node_mode = True

def delete_segment_manual():
    origin = simpledialog.askstring("Nodo origen", "Introduce el nombre del nodo origen:", parent=root)
    dest = simpledialog.askstring("Nodo destino", "Introduce el nombre del nodo destino:", parent=root)
    if not origin or not dest:
        return
    seg_to_remove = next((s for s in current_graph.segments if s.origin.name == origin and s.destination.name == dest), None)
    if seg_to_remove:
        current_graph.segments.remove(seg_to_remove)
        if seg_to_remove.destination in seg_to_remove.origin.list_of_neighbors:
            seg_to_remove.origin.list_of_neighbors.remove(seg_to_remove.destination)
        messagebox.showinfo("Segmento eliminado", f"Se eliminó el segmento de {origin} a {dest}.", parent=root)
        draw_graph()
    else:
        messagebox.showerror("Error", "No se encontró el segmento.", parent=root)

def delete_segment_click():
    global click_delete_segment_mode
    click_delete_segment_mode = True

def show_neighbors():
    name = simpledialog.askstring("Ver vecinos", "Introduce el nombre del nodo:", parent=root)
    if not name:
        return

    origin = next((n for n in current_graph.nodes if n.name == name), None)
    if origin is None:
        messagebox.showerror("Error", f"No se encontró el nodo '{name}'.", parent=root)
        return

    fig, ax = plt.subplots()
    ax.set_title(f"Vecinos de {name}")
    ax.axis("equal")
    ax.grid(True)

    # Dibujar todos los segmentos en negro primero
    for seg in current_graph.segments:
        x1, y1 = seg.origin.x, seg.origin.y
        x2, y2 = seg.destination.x, seg.destination.y
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black"))
        ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8)

    # Dibujar los segmentos salientes del nodo origen hacia sus vecinos (por encima, en rojo)
    for neighbor in origin.list_of_neighbors:
        seg = next((s for s in current_graph.segments if s.origin == origin and s.destination == neighbor), None)
        if seg:
            x1, y1 = seg.origin.x, seg.origin.y
            x2, y2 = seg.destination.x, seg.destination.y
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color="red", lw=2.0))
            ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8, color="red")

    # Dibujar nodos con colores
    for node in current_graph.nodes:
        if node == origin:
            ax.plot(node.x, node.y, "o", color="blue")  # Origen
        elif node in origin.list_of_neighbors:
            ax.plot(node.x, node.y, "o", color="green")  # Vecino
        else:
            ax.plot(node.x, node.y, "o", color="gray")   # Otros
        ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=9)

    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.mpl_connect("button_press_event", on_graph_click)

    globals()['current_canvas'] = canvas


def show_shortest_path():
    global current_graph, current_canvas
    if current_graph is None:
        tk.messagebox.showwarning("Grafo no cargado", "Primero crea o carga un grafo.")
        return

    origin = simpledialog.askstring("Camino más corto", "Introduce el nodo de origen:", parent=root)
    destination = simpledialog.askstring("Camino más corto", "Introduce el nodo de destino:", parent=root)

    if not origin or not destination:
        return

    path = FindShortestPath(current_graph, origin, destination)

    if path is None or not path.nodes:
        tk.messagebox.showinfo("Sin camino", f"No hay camino posible entre {origin} y {destination}.")
        return

    # Pedimos a PlotPath que nos devuelva el gráfico ya preparado
    fig = PlotPath(current_graph, path)

    # Sustituimos el gráfico actual en la interfaz
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.mpl_connect("button_press_event", on_graph_click)

    globals()['current_canvas'] = canvas



def show_reachability():
    global current_graph
    if current_graph is None:
        tk.messagebox.showwarning("Grafo no cargado", "Primero crea o carga un grafo.")
        return

    origin_name = simpledialog.askstring("Nodo origen", "Introduce el nombre del nodo:", parent=root)
    if not origin_name:
        return

    origin = next((n for n in current_graph.nodes if n.name == origin_name), None)
    if origin is None:
        tk.messagebox.showerror("Error", f"No se encontró el nodo '{origin_name}'.", parent=root)
        return

    reachable = ReachableNodes(current_graph, origin_name)
    if not reachable:
        tk.messagebox.showinfo("Accesibilidad", f"No hay nodos alcanzables desde '{origin_name}'.")
        return

    fig, ax = plt.subplots()
    ax.set_title(f"Nodos alcanzables desde {origin_name}")
    ax.axis("equal")
    ax.grid(True)

    # Pintar todos los segmentos en negro primero
    for seg in current_graph.segments:
        x1, y1 = seg.origin.x, seg.origin.y
        x2, y2 = seg.destination.x, seg.destination.y
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="black"))
        ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8)

    # Pintar en verde los segmentos que van desde un nodo alcanzable a otro alcanzable (incluido el origen)
    reached_set = set(reachable)
    reached_set.add(origin)
    for seg in current_graph.segments:
        if seg.origin in reached_set and seg.destination in reached_set:
            x1, y1 = seg.origin.x, seg.origin.y
            x2, y2 = seg.destination.x, seg.destination.y
            mx, my = (x1 + x2)/2, (y1 + y2)/2
            ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                        arrowprops=dict(arrowstyle="->", color="green", lw=2.0))
            ax.text(mx, my, f"{seg.cost:.1f}", fontsize=8, color="green")

    # Pintar nodos con colores
    for node in current_graph.nodes:
        if node == origin:
            ax.plot(node.x, node.y, "o", color="blue")
        elif node in origin.list_of_neighbors:
            ax.plot(node.x, node.y, "o", color="green")
        elif node in reachable:
            ax.plot(node.x, node.y, "o", color="orange")
        else:
            ax.plot(node.x, node.y, "o", color="gray")
        ax.text(node.x + 0.3, node.y + 0.3, node.name, fontsize=9)

    # Mostrar en la interfaz
    if current_canvas:
        current_canvas.get_tk_widget().destroy()

    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.mpl_connect("button_press_event", on_graph_click)

    globals()['current_canvas'] = canvas






# Botones
botones = [
    ("Mostrar grafo de ejemplo", show_example_graph),
    ("Mostrar mi grafo inventado", show_custom_graph),
    ("Cargar grafo desde archivo", load_graph_from_file),
    ("Crear grafo vacío", create_empty_graph),
    ("Ver vecinos de un nodo", show_neighbors),
    ("Añadir nodo con clic", add_node_click),
    ("Añadir nodo manualmente", add_node_manual),
    ("Añadir segmento manualmente", add_segment_manual),
    ("Eliminar nodo con clic", delete_node_click),
    ("Eliminar nodo manualmente", delete_node_manual),
    ("Eliminar segmento con clic", delete_segment_click),
    ("Eliminar segmento manualmente", delete_segment_manual),
    ("Camino más corto entre dos nodos", show_shortest_path),
    ("Ver nodos alcanzables", show_reachability),
    ("Guardar grafo en archivo", save_graph_to_file)
]

for text, command in botones:
    btn = tk.Button(left_frame, text=text, command=command, width=30)
    btn.pack(pady=4)

root.mainloop()
