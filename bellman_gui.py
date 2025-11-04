import tkinter as tk
from tkinter import messagebox, scrolledtext
import subprocess  # To run our C program
import random      # For generating random distances
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import networkx as nx  # For graph visualization

class BellmanFordGUI:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Bellman-Ford Shortest Path Visualizer")
        self.root.geometry("1400x850")
        self.root.configure(bg='#f0f0f0')

        # Variables to store our data
        self.city_entries, self.city_names, self.city_count, self.graph_data = [], [], 0, None

        # Create title label at the top with better styling
        title_frame = tk.Frame(root, bg='#2c3e50', pady=15)
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="🗺️ Bellman-Ford Shortest Path Visualizer", 
                font=("Arial", 18, "bold"), bg='#2c3e50', fg='white').pack()

        # Main container to hold left and right panels
        main_container = tk.Frame(root, bg='#f0f0f0')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left panel: for all the controls and inputs
        left_frame = tk.Frame(main_container, bg='#f0f0f0')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Right panel: for graph visualization
        right_frame = tk.Frame(main_container, relief=tk.SOLID, borderwidth=2, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Section 1: Input for number of cities (with better styling)
        input_section = tk.LabelFrame(left_frame, text="📊 Step 1: City Configuration", 
                                      font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                      relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        input_section.pack(pady=5, fill=tk.X)
        
        frame_top = tk.Frame(input_section, bg='#f0f0f0')
        frame_top.pack(pady=5)
        tk.Label(frame_top, text="Number of Cities (2-15):", font=("Arial", 10), 
                bg='#f0f0f0').grid(row=0, column=0, padx=5, sticky='w')
        self.entry_cities = tk.Entry(frame_top, width=10, font=("Arial", 10))
        self.entry_cities.grid(row=0, column=1, padx=5)
        tk.Button(frame_top, text="Create Matrix", command=self.create_matrix, 
                 bg='#3498db', fg='white', font=("Arial", 10, "bold"), 
                 relief=tk.RAISED, padx=10, pady=5).grid(row=0, column=2, padx=5)

        # Section 2: Distance matrix container (with better styling)
        matrix_section = tk.LabelFrame(left_frame, text="📝 Step 2: Distance Matrix", 
                                       font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                       relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        matrix_section.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.matrix_frame = tk.Frame(matrix_section, bg='#f0f0f0')
        self.matrix_frame.pack(pady=5)

        # Button to generate random distances (disabled until matrix is created)
        self.random_btn = tk.Button(matrix_section, text="🎲 Generate Random Distances", 
                                    command=self.randomize_matrix, state="disabled",
                                    bg='#9b59b6', fg='white', font=("Arial", 10, "bold"),
                                    relief=tk.RAISED, padx=10, pady=5)
        self.random_btn.pack(pady=5)

        # Section 3: Source selection and algorithm execution
        control_section = tk.LabelFrame(left_frame, text="🚀 Step 3: Run Algorithm", 
                                       font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                       relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        control_section.pack(pady=5, fill=tk.X)
        
        source_frame = tk.Frame(control_section, bg='#f0f0f0')
        source_frame.pack(pady=5)
        tk.Label(source_frame, text="Select Source City:", font=("Arial", 10), 
                bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
        self.source_var = tk.StringVar()
        self.source_menu = tk.OptionMenu(source_frame, self.source_var, [])
        self.source_menu.config(font=("Arial", 10), width=8)
        self.source_menu.pack(side=tk.LEFT, padx=5)

        # Button to run the algorithm
        tk.Button(control_section, text="▶ Run Algorithm", command=self.run_algorithm,
                 bg='#27ae60', fg='white', font=("Arial", 11, "bold"),
                 relief=tk.RAISED, padx=20, pady=8).pack(pady=10)

        # Section 4: Results display (with better styling)
        results_section = tk.LabelFrame(left_frame, text="📋 Results", 
                                       font=("Arial", 11, "bold"), bg='#f0f0f0', 
                                       relief=tk.GROOVE, borderwidth=2, padx=10, pady=10)
        results_section.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.txt_output = scrolledtext.ScrolledText(results_section, width=50, height=12, 
                                                    font=("Consolas", 9), bg='#ffffff',
                                                    relief=tk.SUNKEN, borderwidth=2)
        self.txt_output.pack(pady=5, fill=tk.BOTH, expand=True)

        # Section 5: Graph visualization area (improved styling)
        graph_header = tk.Frame(right_frame, bg='#34495e', pady=10)
        graph_header.pack(fill=tk.X)
        tk.Label(graph_header, text="🗺️ Network Graph Visualization", 
                font=("Arial", 13, "bold"), bg='#34495e', fg='white').pack()
        
        # Create a matplotlib figure for drawing the graph with more space
        self.fig = Figure(figsize=(7, 7), dpi=100, facecolor='white')
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Show initial message before any graph is created
        self.ax.text(0.5, 0.5, 'Run algorithm to see shortest path visualization', 
                    ha='center', va='center', fontsize=12, color='#7f8c8d', style='italic')
        self.ax.set_xlim(0, 1); self.ax.set_ylim(0, 1); self.ax.axis('off'); self.canvas.draw()

    def create_matrix(self):
        """Creates the distance matrix based on user input"""
        try:
            # Get the number of cities from the entry box and validate
            self.city_count = int(self.entry_cities.get())
            if not 2 <= self.city_count <= 15:
                messagebox.showerror("Error", "Enter 2-15 cities"); return
        except ValueError:
            messagebox.showerror("Error", "Invalid number"); return

        # Clear any existing matrix
        for widget in self.matrix_frame.winfo_children(): widget.destroy()
        self.city_entries.clear()

        # Auto-generate city names: A, B, C, D, etc. (chr(65) = 'A')
        self.city_names = [chr(65 + i) for i in range(self.city_count)]

        # Add instruction label and column headers
        tk.Label(self.matrix_frame, text="Enter distances (0 = same city, INF = no direct road)", 
                font=("Arial", 9, "italic"), bg='#f0f0f0', fg='#555').grid(
                row=0, column=0, columnspan=self.city_count+1, pady=5)
        # Column headers
        tk.Label(self.matrix_frame, text="", bg='#f0f0f0').grid(row=1, column=0)  # Empty corner
        for j, name in enumerate(self.city_names):
            tk.Label(self.matrix_frame, text=name, font=("Arial", 10, "bold"), 
                    bg='#3498db', fg='white', width=5, relief=tk.RAISED).grid(
                    row=1, column=j+1, padx=1, pady=1)

        # Create the matrix grid with entry boxes (improved styling)
        for i, name in enumerate(self.city_names):
            # Row headers
            tk.Label(self.matrix_frame, text=name, font=("Arial", 10, "bold"), 
                    bg='#3498db', fg='white', width=5, relief=tk.RAISED).grid(
                    row=i+2, column=0, padx=1, pady=1)
            row_entries = []
            for j in range(self.city_count):
                e = tk.Entry(self.matrix_frame, width=6, justify="center", font=("Arial", 9))
                e.grid(row=i+2, column=j+1, padx=1, pady=1)
                if i == j:
                    e.insert(0, "0")
                    e.config(state='readonly', readonlybackground='#ecf0f1')  # Diagonal is read-only
                else:
                    e.insert(0, "")
                row_entries.append(e)
            self.city_entries.append(row_entries)

        # Update the source city dropdown menu
        self.source_var.set(self.city_names[0])
        menu = self.source_menu["menu"]
        menu.delete(0, "end")
        for name in self.city_names:
            menu.add_command(label=name, command=lambda v=name: self.source_var.set(v))
        self.random_btn.config(state="normal")  # Enable the random button










    # ...existing code...
    def draw_graph(self, highlight_source=None, shortest_distances=None):
        """Draw road-style visualization: clearer city labels & fit whole graph in frame."""
        from matplotlib.lines import Line2D
        from matplotlib.patches import Circle

        self.ax.clear()
        self.txt_output.tag_config("warn", foreground="red")

        # Placeholder
        if not (highlight_source and shortest_distances):
            self.ax.set_facecolor('#f6fbff')
            self.ax.text(0.5, 0.5, 'Run algorithm to see shortest path visualization',
                         ha='center', va='center', fontsize=12, color='#7f8c8d', style='italic')
            self.ax.set_xlim(-1, 11); self.ax.set_ylim(-10, 10); self.ax.axis('off'); self.canvas.draw()
            return

        # Build directed edges from the matrix
        all_edges = {}
        for i in range(self.city_count):
            for j in range(self.city_count):
                val = self.city_entries[i][j].get().strip().upper()
                if val and val != "INF":
                    try:
                        w = int(val)
                    except ValueError:
                        continue
                    if not (i == j and w == 0):
                        all_edges[(self.city_names[i], self.city_names[j])] = w

        source = highlight_source
        destinations = [c for c in self.city_names if c != source]
        n_dest = len(destinations)
        y_spacing = 2.0

        # Reconstruct paths
        all_paths = []
        verification_messages = []
        for idx, dest in enumerate(destinations):
            y_pos = (idx - (n_dest - 1) / 2) * y_spacing
            dest_dist = shortest_distances.get(dest, float('inf'))
            if dest_dist == float('inf'):
                all_paths.append((dest, [source, dest], [], y_pos, dest_dist))
                continue

            path = [dest]; current = dest; safe_break = 0
            while current != source and safe_break < (self.city_count * 2):
                safe_break += 1; found = False
                for p in self.city_names:
                    if p == current: continue
                    if (p, current) in all_edges:
                        w = all_edges[(p, current)]
                        p_dist = shortest_distances.get(p, float('inf'))
                        cur_dist = shortest_distances.get(current, float('inf'))
                        if p_dist != float('inf') and p_dist + w == cur_dist:
                            path.insert(0, p); current = p; found = True; break
                if not found: break

            if path[0] != source:
                all_paths.append((dest, [source, dest], [], y_pos, dest_dist)); continue

            path_edges = [(path[i], path[i+1], all_edges.get((path[i], path[i+1]), 0))
                          for i in range(len(path) - 1)]
            sum_w = sum(w for _, _, w in path_edges)
            if sum_w != dest_dist:
                verification_messages.append(f"⚠ Path to {dest}: sum={sum_w} vs reported={dest_dist}")
            all_paths.append((dest, path, path_edges, y_pos, dest_dist))

        # Drawing parameters
        self.ax.set_facecolor('#f6fbff')
        node_radius = 0.45
        src_x = 0.8
        max_x = 10.0
        all_x = []
        all_y = []

        # Draw each path as a road
        for dest, path_nodes, path_edges, y_pos, dest_dist in all_paths:
            path_len = len(path_nodes)
            xs = []; ys = []
            for i in range(path_len):
                if i == 0:
                    x = src_x
                else:
                    x = max_x if (path_len - 1 == 1) else src_x + (max_x - src_x) * (i) / (path_len - 1)
                xs.append(x); ys.append(y_pos)
                all_x.append(x); all_y.append(y_pos)

            # Road base
            road_line = Line2D(xs, ys, linewidth=18, color='#3f3f3f', solid_capstyle='round', zorder=1, alpha=0.97)
            self.ax.add_line(road_line)
            # Road edges
            self.ax.add_line(Line2D(xs, [y - 0.28 for y in ys], linewidth=2.4, color='#7a7a7a', solid_capstyle='round', zorder=1.1, alpha=0.6))
            self.ax.add_line(Line2D(xs, [y + 0.28 for y in ys], linewidth=2.4, color='#7a7a7a', solid_capstyle='round', zorder=1.1, alpha=0.6))
            # Center dashed lane
            self.ax.add_line(Line2D(xs, ys, linewidth=2.0, color='white', linestyle=(0, (10, 8)), solid_capstyle='round', zorder=2, alpha=0.95))

            # Draw nodes + labels (name inside node, distance badge to the right)
            for i, node_name in enumerate(path_nodes):
                x = xs[i]; y = ys[i]
                # shadow
                self.ax.add_patch(Circle((x + 0.10, y - 0.10), node_radius + 0.12, color='#000', alpha=0.06, zorder=3))
                if i == 0:
                    face, edgec = '#FF6B6B', '#CC2E2E'
                    size = node_radius + 0.05
                else:
                    reachable = (dest_dist != float('inf'))
                    if node_name == dest:
                        face = '#44FF44' if reachable else '#88B3FF'; edgec = '#00AA00' if reachable else '#0066CC'
                        size = node_radius
                    else:
                        face = '#DFF5E0' if dest_dist != float('inf') else '#E6E9EE'; edgec = '#A3C293' if dest_dist != float('inf') else '#BFC9CA'
                        size = node_radius * 0.85
                self.ax.add_patch(Circle((x, y), size, facecolor=face, edgecolor=edgec, linewidth=1.4, zorder=4))

                # Name inside node (clear, bold, clipped)
                self.ax.text(x, y, node_name, ha='center', va='center', fontsize=10, fontweight='bold',
                             color='#1b2733', zorder=5)

                # Distance badge to the right of node (small rounded bbox)
                node_dist = shortest_distances.get(node_name, float('inf'))
                dtext = '∞' if node_dist == float('inf') else str(int(node_dist))
                badge_x = x + size + 0.22
                self.ax.text(badge_x, y, dtext, ha='center', va='center', fontsize=8, color='#1b2733', zorder=6,
                             bbox=dict(boxstyle='round,pad=0.18', facecolor='white', edgecolor='#d0d5d9', alpha=0.95))

        # Auto-set limits so whole graph fits with padding
        if all_x and all_y:
            min_x = min(all_x); max_xv = max(all_x)
            min_y = min(all_y); max_y = max(all_y)
            x_pad = max(1.0, (max_xv - min_x) * 0.08)
            y_pad = max(1.0, (max_y - min_y) * 0.18)
            self.ax.set_xlim(min_x - x_pad, max_xv + x_pad)
            self.ax.set_ylim(min_y - y_pad, max_y + y_pad)
        else:
            self.ax.set_xlim(-0.5, max_x + 0.5)
            self.ax.set_ylim(- (n_dest - 1) * y_spacing / 2 - 2, (n_dest - 1) * y_spacing / 2 + 2)

        # Title and legend
        reachable_count = sum(1 for d in shortest_distances.values() if d != float('inf')) - 1
        total_cities = len(self.city_names) - 1
        title_text = f"Road-style Paths from {source}  —  Reachable: {reachable_count}/{total_cities}"
        self.ax.set_title(title_text, fontsize=12, fontweight='bold', pad=12, color='#2c3e50')

        legend_items = [
            (plt.Line2D([0], [0], color='#3f3f3f', linewidth=6), "Road"),
            (plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#FF6B6B', markersize=8, markeredgecolor='#CC2E2E'), "Source"),
            (plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#44FF44', markersize=7, markeredgecolor='#00AA00'), "Destination (Reachable)"),
            (plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#88B3FF', markersize=7, markeredgecolor='#0066CC'), "Destination (Unreachable)")
        ]
        handles, labels = zip(*legend_items)
        self.ax.legend(handles=handles, labels=labels, loc='upper center', bbox_to_anchor=(0.5, -0.03),
                       ncol=4, frameon=True, fancybox=True, shadow=False, fontsize=9, framealpha=0.95)

        # Verification warnings
        if verification_messages:
            self.txt_output.insert(tk.END, "\n", "warn")
            for msg in verification_messages:
                self.txt_output.insert(tk.END, msg + "\n", "warn")

        self.ax.axis('off')
        self.fig.tight_layout()
        self.canvas.draw()
# ...existing code...
    















    def randomize_matrix(self):
        """Fill the matrix with random distances for quick testing"""
        for i in range(self.city_count):
            for j in range(self.city_count):
                if i != j:  # Skip diagonal (read-only)
                    self.city_entries[i][j].delete(0, tk.END)
                    self.city_entries[i][j].insert(0, str(random.randint(1, 50)))
        # Don't draw graph yet - only after running algorithm
        self.txt_output.delete("1.0", tk.END)
        self.txt_output.insert(tk.END, "Random distances generated. Select source city and run algorithm.\n")

    def run_algorithm(self):
        """Main function to run the Bellman-Ford algorithm using C backend"""
        if not self.city_names:
            messagebox.showerror("Error", "Create city matrix first"); return

        # Build list of edges from the matrix
        edges = []
        for i in range(self.city_count):
            for j in range(self.city_count):
                val = self.city_entries[i][j].get().strip().upper()
                if val and val not in ["", "INF", "0"]:
                    try: edges.append(f"{self.city_names[i]} {self.city_names[j]} {int(val)}")
                    except ValueError: continue

        if not edges:
            messagebox.showerror("Error", "No valid distances"); return

        # Prepare input data in the format C program expects
        src_city = self.source_var.get()
        V, E = self.city_count, len(edges)
        data = f"{V} {E}\n" + "\n".join(self.city_names) + "\n" + "\n".join(edges) + "\n" + src_city + "\n"

        try:
            # Run the C program using subprocess - THIS IS WHERE ALGORITHM RUNS
            result = subprocess.run(["./bellman_backend.exe"], input=data, text=True, capture_output=True)
            self.txt_output.delete("1.0", tk.END); self.txt_output.insert(tk.END, result.stdout)  # Display C output
            self.parse_and_visualize_results(result.stdout, src_city)  # Parse and visualize
        except FileNotFoundError:
            messagebox.showerror("Error", "Compile C program: gcc bellman_backend.c -o bellman_backend.exe")

    def parse_and_visualize_results(self, output, source_city):
        """Parse the C program output and update graph with results"""
        shortest_distances = {}
        lines = [ln for ln in output.strip().split('\n') if ln.strip()]
        parsing = False
        for line in lines:
            if 'Source City:' in line:
                # next lines include table heading; start parsing after the next '----' line
                parsing = False
                continue
            if '------------------------------------' in line:
                parsing = not parsing
                continue
            if parsing and line.strip():
                parts = line.split()
                if len(parts) >= 2 and parts[0] in self.city_names:
                    city, dist_str = parts[0], parts[1]
                    shortest_distances[city] = float('inf') if dist_str == 'INF' else int(dist_str) if dist_str.lstrip('-').isdigit() else None

        # As a fallback if parsing failed to capture the distances (some C outputs vary), try a simple extraction
        if not shortest_distances:
            for n in self.city_names:
                # try to find a line like: "A              0"
                for line in lines:
                    if line.strip().startswith(n + ' '):
                        parts = line.split()
                        if len(parts) >= 2 and parts[0] == n:
                            d = parts[1]
                            shortest_distances[n] = float('inf') if d == 'INF' else int(d) if d.lstrip('-').isdigit() else None

        # ensure source included
        if source_city not in shortest_distances:
            shortest_distances[source_city] = 0

        self.graph_data = True; self.draw_graph(highlight_source=source_city, shortest_distances=shortest_distances)

# Main program starts here
if __name__ == "__main__":
    root = tk.Tk()  # Create the main window
    app = BellmanFordGUI(root)  # Create our GUI application
    root.mainloop()  # Start the GUI event loop
    
