import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# ---------------- Bellman-Ford Algorithm ----------------
def bellman_ford(V, edges, source_index):
    INF = float('inf')
    dist = [INF] * V
    parent = [-1] * V
    dist[source_index] = 0

    for _ in range(V - 1):
        for (u, v, w) in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u

    # Check for negative weight cycles
    for (u, v, w) in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            messagebox.showerror("Error", "Graph contains a negative weight cycle!")
            return None, None

    return dist, parent

# ---------------- Visualization ----------------
def visualize_graph(city_names, edges, dist, parent, source_index):
    G = nx.DiGraph()

    for (u, v, w) in edges:
        G.add_edge(city_names[u], city_names[v], weight=w)

    pos = nx.spring_layout(G, k=0.8, seed=42)
    colors = []

    for node in G.nodes():
        if node == city_names[source_index]:
            colors.append('red')
        else:
            colors.append('skyblue')

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000,
            font_size=10, edgecolors='black', arrows=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title(f"Shortest Paths from {city_names[source_index]}")
    plt.show()

# ---------------- GUI Class ----------------
class RoutePlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimal Route Planner")
        self.root.geometry("900x700")
        self.root.configure(bg="#f5f5f5")

        self.city_names = []
        self.edges = []
        self.V = 0

        self.create_intro_screen()

    # Step 1: Number of cities
    def create_intro_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Optimal Route Planner", font=("Helvetica", 22, "bold"), bg="#f5f5f5").pack(pady=30)
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack()

        tk.Label(frame, text="Enter number of cities:", font=("Arial", 14), bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=10)
        self.num_entry = tk.Entry(frame, font=("Arial", 14), width=10)
        self.num_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Next", command=self.get_city_names,
                  font=("Arial", 12), bg="#4CAF50", fg="white", width=15).pack(pady=20)

    # Step 2: City names
    def get_city_names(self):
        try:
            self.V = int(self.num_entry.get())
            if self.V <= 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number (>1)")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter City Names", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=20)
        frame = tk.Frame(self.root, bg="#f5f5f5")
        frame.pack()

        self.city_entries = []
        for i in range(self.V):
            tk.Label(frame, text=f"City {i+1}:", bg="#f5f5f5").grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(frame, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.city_entries.append(entry)

        tk.Button(self.root, text="Next", command=self.get_road_details,
                  font=("Arial", 12), bg="#4CAF50", fg="white", width=15).pack(pady=20)

    # Step 3: Add roads (Source, Destination, Distance)
    def get_road_details(self):
        self.city_names = [e.get().strip() for e in self.city_entries]
        if any(name == "" for name in self.city_names):
            messagebox.showerror("Error", "All city names must be filled!")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Enter Roads / Paths (Like Source → Destination → Distance)",
                 font=("Helvetica", 15, "bold"), bg="#f5f5f5").pack(pady=20)

        form_frame = tk.Frame(self.root, bg="#f5f5f5")
        form_frame.pack()

        tk.Label(form_frame, text="Source City:", bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5)
        self.src_var = tk.StringVar()
        self.src_combo = ttk.Combobox(form_frame, textvariable=self.src_var, values=self.city_names, width=20)
        self.src_combo.grid(row=0, column=1)

        tk.Label(form_frame, text="Destination City:", bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5)
        self.dest_var = tk.StringVar()
        self.dest_combo = ttk.Combobox(form_frame, textvariable=self.dest_var, values=self.city_names, width=20)
        self.dest_combo.grid(row=1, column=1)

        tk.Label(form_frame, text="Distance:", bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5)
        self.dist_entry = tk.Entry(form_frame, width=10)
        self.dist_entry.grid(row=2, column=1, pady=5)

        tk.Button(self.root, text="Add Road", command=self.add_road,
                  font=("Arial", 12), bg="#2196F3", fg="white", width=15).pack(pady=10)

        self.road_list = tk.Listbox(self.root, width=50, height=10, font=("Arial", 10))
        self.road_list.pack(pady=10)

        tk.Button(self.root, text="Next → Select Source", command=self.show_source_selection,
                  font=("Arial", 12), bg="#4CAF50", fg="white", width=20).pack(pady=15)

    def add_road(self):
        src = self.src_var.get()
        dest = self.dest_var.get()
        dist = self.dist_entry.get()

        if src == "" or dest == "" or dist == "":
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        if src == dest:
            messagebox.showwarning("Warning", "Source and Destination cannot be same!")
            return

        try:
            distance = int(dist)
        except ValueError:
            messagebox.showerror("Error", "Distance must be an integer!")
            return

        src_index = self.city_names.index(src)
        dest_index = self.city_names.index(dest)
        self.edges.append((src_index, dest_index, distance))

        self.road_list.insert(tk.END, f"{src} → {dest} : {distance}")
        self.dist_entry.delete(0, tk.END)

    # Step 4: Select source city
    def show_source_selection(self):
        if not self.edges:
            messagebox.showerror("Error", "Please add at least one road!")
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Select Source City", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=20)

        self.source_var = tk.StringVar()
        self.source_combo = ttk.Combobox(self.root, textvariable=self.source_var, values=self.city_names, font=("Arial", 12))
        self.source_combo.pack(pady=10)
        self.source_combo.current(0)

        tk.Button(self.root, text="Show Result", command=self.show_result,
                  font=("Arial", 12), bg="#4CAF50", fg="white", width=15).pack(pady=20)

    # Step 5: Show result table and graph
    def show_result(self):
        src_name = self.source_var.get()
        src_index = self.city_names.index(src_name)

        dist, parent = bellman_ford(self.V, self.edges, src_index)
        if dist is None:
            return

        result_data = {"City": self.city_names, "Distance": ["INF" if d == float('inf') else d for d in dist]}
        df = pd.DataFrame(result_data)

        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"Shortest Distances from {src_name}", font=("Helvetica", 18, "bold"), bg="#f5f5f5").pack(pady=10)

        tree = ttk.Treeview(self.root, columns=("City", "Distance"), show="headings", height=self.V)
        tree.heading("City", text="City")
        tree.heading("Distance", text="Distance")
        tree.column("City", width=200)
        tree.column("Distance", width=150)
        tree.pack(pady=20)

        for _, row in df.iterrows():
            tree.insert("", "end", values=(row["City"], row["Distance"]))

        tk.Button(self.root, text="Show Graph", command=lambda: visualize_graph(self.city_names, self.edges, dist, parent, src_index),
                  font=("Arial", 12), bg="#2196F3", fg="white", width=15).pack(pady=10)

        tk.Button(self.root, text="Restart", command=self.create_intro_screen,
                  font=("Arial", 12), bg="#9E9E9E", fg="white", width=10).pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = RoutePlannerApp(root)
    root.mainloop()
