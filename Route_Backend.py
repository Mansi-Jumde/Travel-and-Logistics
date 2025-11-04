import sys
from typing import Dict, List, Tuple

class Edge:
    def __init__(self, src=0, dest=0, weight=0):
        self.src = src
        self.dest = dest 
        self.weight = weight

class Graph:
    def __init__(self, V: int, E: int):
        self.V = V
        self.E = E
        self.edge = [Edge() for _ in range(E)]
        self.distance_cache: Dict[int, List[int]] = {}

    def bellman_ford(self, src: int, city_names: List[str]) -> List[int]:
        """Bellman-Ford with memoization"""
        if src in self.distance_cache:
            print(f"\nUsing cached result for source: {city_names[src]}")
            return self.distance_cache[src]

        dist = [sys.maxsize] * self.V
        dist[src] = 0
        
        for _ in range(self.V - 1):
            for j in range(self.E):
                u = self.edge[j].src
                v = self.edge[j].dest
                w = self.edge[j].weight
                if dist[u] != sys.maxsize and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w

        # Check for negative cycles
        for j in range(self.E):
            u = self.edge[j].src
            v = self.edge[j].dest
            w = self.edge[j].weight
            if dist[u] != sys.maxsize and dist[u] + w < dist[v]:
                print("\nWarning: Graph contains negative weight cycle!")
                return dist

        self.distance_cache[src] = dist.copy()
        return dist

def save_results(dist: List[int], city_names: List[str], src: int):
    """Save results to CSV files for visualization"""
    # Save results
    with open("route_results.csv", "w") as f:
        f.write("Source,Destination,Distance\n")
        for i in range(len(dist)):
            distance = "INF" if dist[i] == sys.maxsize else str(dist[i])
            f.write(f"{city_names[src]},{city_names[i]},{distance}\n")

def main():
    try:
        print("\n🌟 Bellman-Ford Shortest Path Calculator")
        print("=" * 40)
        
        # Get input
        V, E = map(int, input("\nEnter number of cities and roads (e.g., 4 5): ").split())
        if V < 2 or E < 1:
            raise ValueError("Need at least 2 cities and 1 road")
            
        graph = Graph(V, E)
        city_names = []

        print("\n📍 Enter city names:")
        for i in range(V):
            city = input(f"City {i + 1}: ").strip()
            if not city:
                raise ValueError("City name cannot be empty")
            city_names.append(city)

        print("\n🛣️ Enter roads as: SourceCity DestinationCity Distance")
        print("Example: London Paris 350")
        
        # Save edges for visualization
        with open("route_edges.csv", "w") as f:
            f.write("Source,Destination,Weight\n")
            
            for i in range(E):
                try:
                    src, dest, weight = input(f"Road {i + 1}: ").split()
                    weight = int(weight)
                    
                    try:
                        src_idx = city_names.index(src)
                        dest_idx = city_names.index(dest)
                    except ValueError:
                        print(f"Error: City '{src}' or '{dest}' not found!")
                        continue
                        
                    graph.edge[i] = Edge(src_idx, dest_idx, weight)
                    f.write(f"{src},{dest},{weight}\n")
                    
                except ValueError:
                    print("Error: Invalid input format! Use: City1 City2 Distance")
                    return

        while True:
            src_city = input("\nEnter source city (or 'quit' to exit): ").strip()
            if src_city.lower() == 'quit':
                break

            try:
                src_idx = city_names.index(src_city)
            except ValueError:
                print("Error: City not found!")
                continue

            # Run algorithm
            distances = graph.bellman_ford(src_idx, city_names)
            
            # Print results
            print("\nShortest Distances:")
            print("-" * 30)
            for i, dist in enumerate(distances):
                if dist == sys.maxsize:
                    print(f"{city_names[i]:<15} : INF")
                else:
                    print(f"{city_names[i]:<15} : {dist}")

            # Save results for visualization
            save_results(distances, city_names, src_idx)
            print("\n✅ Results saved for visualization")
            print("Run 'python Route_Visualizer.py' to see the graph")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    main()

































