# Travel-and-Logistics

A Python-based project that calculates and visualizes the shortest route between cities using the Bellman-Ford algorithm.
It handles negative edge weights, detects negative cycles, and provides an interactive visualization of computed routes.

 Overview

This project models a transportation or network system as a weighted directed graph, where:

Nodes (Vertices) represent cities

Edges (Weights) represent roads and their distances

It consists of two main Python modules:

Route_Backend.py – Computes the shortest paths using the Bellman-Ford algorithm with memoization.

Route_Visualizer.py – Reads stored route data and visualizes it using NetworkX and Matplotlib.

Objectives

-Implement the Bellman-Ford Algorithm for route optimization.

-Support negative edge weights and negative cycle detection.

-Use memoization to avoid redundant recalculations.

-Export computed routes to CSV files for later visualization.

-Provide graphical output of the optimal paths between cities.

Algorithm & Techniques

Algorithm Used: Bellman-Ford Algorithm with Memoization

Key Techniques:

Dynamic Programming : Repeated edge relaxation to compute shortest distances
Memoization	:  Stores computed paths for reuse
CSV File Handling :	Exports and imports route data
NetworkX :	Builds and analyzes directed weighted graphs
Matplotlib : Visualizes graph connections and routes
Pandas :	Efficiently handles CSV input/output

Time Complexity: O(V × E) — efficient for small and medium networks.

Future Scope
-Develop a GUI using Tkinter or Streamlit.

-Integrate with Google Maps API or OpenStreetMap.

-Extend to Floyd–Warshall Algorithm for all-pairs shortest paths.

-Deploy as a web application using Flask or FastAPI.

-Incorporate real-time traffic updates via external APIs.

Contributors

Mansi Jumde (2nd year, CSE core, Sec: A3,Roll No: 09, Batch: B1)

Khushab Likhitker (2nd year, CSE core, Sec: A3, Roll No: 07, Sec: A3, Batch: B1)

Radhika Joshi (2nd year, CSE core, Sec: A3, Roll No: 35, Sec: A3, Batch: B3)
