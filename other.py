import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq

# Romania cities dictionary
romania_map = {
    'Arad': {'Zerind': 75, 'Timisoara': 118, 'Sibiu': 140},
    'Zerind': {'Oradea': 71, 'Arad': 75},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Dobreta': 75},
    'Dobreta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Dobreta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Sibiu': {'Oradea': 151, 'Arad': 140, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

# City positions for better visualization
pos = {
        'Arad': (-3, 6), 'Zerind': (-2, 8), 'Oradea': (0, 10), 'Timisoara': (-3, 3),
        'Lugoj': (0, 2), 'Mehadia': (0, 0), 'Dobreta': (0, -2), 'Craiova': (4, -2),
        'Sibiu': (3, 5), 'Fagaras': (7, 5), 'Rimnicu Vilcea': (4, 3), 'Pitesti': (7, 2),
        'Bucharest': (10, 0), 'Giurgiu': (9, -2), 'Urziceni': (13, 1), 'Hirsova': (17, 0),
        'Eforie': (19, -2), 'Vaslui': (15, 5), 'Iasi': (13, 7), 'Neamt': (10, 8)
        }


def uniform_cost_search(start, goal):
    queue = [(0, start, [])] # Initialize heap
    visited = set()

    while queue:
        cost, city, path = heapq.heappop(queue) # Pop current element and get all info about it

        if city in visited: # If city was visited then we skip this path
            continue

        path = path + [city] # Add new city to path
        visited.add(city) # Add it to visited set

        if city == goal: # If it is the goal we return
            return path, cost

        for neighbor, distance in romania_map.get(city, {}).items(): # Iteration to get neighbours and update queue
            if neighbor not in visited: # If we didn't visit de neighbour the queue is updated with the cost of neighbour and updating it to current city
                heapq.heappush(queue, (cost + distance, neighbor, path))

    return None, float('inf')


class UCSVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Uniform Cost Search - Romania Cities")
        self.root.geometry("1600x1000")

        # Configure the root grid to center the content
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)

        frame = tk.Frame(root)
        frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Start City label and combobox
        tk.Label(frame, text="Start City:", font=("Arial", 12)).grid(row=0, column=0, sticky="e", padx=10)
        self.start_var = tk.StringVar()
        self.start_menu = ttk.Combobox(frame, textvariable=self.start_var, values=list(romania_map.keys()),
                                       font=("Arial", 12), width=20)
        self.start_menu.grid(row=0, column=1, padx=10, pady=5)

        # Goal City label and combobox
        tk.Label(frame, text="Goal City:", font=("Arial", 12)).grid(row=1, column=0, sticky="e", padx=10)
        self.goal_var = tk.StringVar()
        self.goal_menu = ttk.Combobox(frame, textvariable=self.goal_var, values=list(romania_map.keys()),
                                      font=("Arial", 12), width=20)
        self.goal_menu.grid(row=1, column=1, padx=10, pady=5)

        # button
        self.search_button = tk.Button(frame, text="Find Shortest Path", command=self.run_ucs, font=("Arial", 12),
                                       bg="#4CAF50", fg="white", width=20)
        self.search_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Result label
        self.result_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
        self.result_label.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        # Bottom section (Graph Display Area)
        self.figure, self.ax = plt.subplots(figsize=(10, 7))
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().grid(row=2, column=1, padx=10, pady=10, sticky="nsew")


        self.canvas.get_tk_widget().config(width=1000, height=600)
        self.canvas.get_tk_widget().grid_propagate(False)  # Prevent resizing

        self.draw_graph()

    def run_ucs(self):
        start = self.start_var.get()
        goal = self.goal_var.get()

        # Error handling for missing or invalid city selections
        if not start or not goal:
            self.result_label.config(text="Please select both start and goal cities.", fg="red")
            return
        if start == goal:
            self.result_label.config(text="Start and goal cities cannot be the same.", fg="red")
            return

        try:
            path, cost = uniform_cost_search(start, goal)
            if path:
                self.result_label.config(text=f"Path: {' -> '.join(path)} (Cost: {cost})", fg="blue")
                self.draw_graph(path)
            else:
                self.result_label.config(text="No path found.", fg="red")
        except Exception as e:
            self.result_label.config(text=f"An error occurred: {str(e)}", fg="red")

    def draw_graph(self, path=None):
        try:
            self.ax.clear()  # Clear the previous graph
            G = nx.Graph()

            # Add edges with weights to the graph
            for city, neighbors in romania_map.items():
                for neighbor, distance in neighbors.items():
                    G.add_edge(city, neighbor, weight=distance)



            nx.draw(G, pos, ax=self.ax, with_labels=True, node_size=800, node_color='lightblue',
                    edge_color='gray', font_size=10, font_weight='bold')

            edge_labels = nx.get_edge_attributes(G, 'weight')
            if edge_labels:
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black', font_size=10,
                                             bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

            if path:
                # Highlight the path edges
                path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='green',
                                       width=2.5)
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color="yellow", node_size=900)

                # Highlight path edge labels
                path_edge_labels = {(u, v): edge_labels.get((u, v), edge_labels.get((v, u)))
                                    for u, v in path_edges if (u, v) in edge_labels or (v, u) in edge_labels}

                nx.draw_networkx_edge_labels(G, pos, edge_labels=path_edge_labels, font_color='white', font_size=10,
                                                 bbox=dict(facecolor='red', edgecolor='none', alpha=0.7))

            self.canvas.draw()
        except Exception as e:
            self.result_label.config(text=f"Error drawing the graph: {str(e)}", fg="red")
