# MazeRunner

An interactive maze generator and pathfinding visualizer built with Python and Pygame. Generate random mazes and watch BFS, DFS, A*, and Ant Colony Optimization (ACO) algorithms solve them in real time.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)

## Features

- **Randomized Maze Generation** — Prim's algorithm variant that carves paths through a grid, producing unique solvable mazes every run
- **BFS Solver** — Breadth-first search with wave-propagation visualization; guarantees the shortest path
- **DFS Solver** — Depth-first search with backtracking; explores paths exhaustively and highlights the solution
- **A\* Solver** — A* search with Manhattan distance heuristic; guarantees the shortest path while exploring fewer cells than BFS by prioritizing cells closer to the goal
- **ACO Solver** — Ant Colony Optimization with pheromone trail visualization; a swarm-intelligence metaheuristic where simulated ants probabilistically explore the maze, depositing pheromone on successful paths. Over multiple iterations, pheromone accumulates on shorter routes and evaporates from longer ones, producing emergent convergence toward the optimal path
- **Multi-Checkpoint Routing** — Place intermediate waypoints and route through them with any algorithm
- **Real-time Animation** — Watch each algorithm explore the maze cell by cell, with color-coded states:
  - ⬜ White — open path
  - ⬛ Black — wall
  - 🟦 Blue — start / solution path
  - 🟥 Red — end
  - 🟩 Green — checkpoint
  - 🟨 Yellow — visited (BFS/DFS exploration)
  - 🟧 Orange — visited (A* exploration)
  - 🟪 Purple — pheromone trail (ACO exploration, intensity = pheromone concentration)

## How It Works

### Maze Generation
The generator starts from a seed cell and uses a randomized variant of Prim's algorithm. It maintains a frontier of candidate cells, randomly selects one, carves a passage to an adjacent visited cell, and repeats until every cell is reachable.

### BFS (Breadth-First Search)
Explores all neighbors at the current depth before moving deeper. Uses a wavefront that expands outward from the start, guaranteeing the shortest path. Each cell stores its distance, and the path is reconstructed by tracing back from the end.

### DFS (Depth-First Search)
Uses a stack to explore as deep as possible along each branch before backtracking. Visited dead-ends are marked and skipped. The final path is the stack contents when the end is reached.

### A* Search
Combines the shortest-path guarantee of BFS with a heuristic that steers exploration toward the goal. Uses f(n) = g(n) + h(n), where g(n) is the actual distance from the start and h(n) is the Manhattan distance to the goal. Explores significantly fewer cells than BFS on most mazes while still finding the optimal path.

### ACO (Ant Colony Optimization)
A swarm-intelligence metaheuristic inspired by how real ants find shortest paths. Multiple simulated ants walk from start to end, choosing neighbors probabilistically based on pheromone concentration (exploitation) and inverse Manhattan distance to the goal (exploration). After each iteration, pheromone is deposited on successful paths (shorter paths receive more) and the entire grid evaporates slightly. Over 50 iterations, pheromone accumulates on the best routes, and the shortest path found across all iterations is displayed. The purple gradient visualization shows pheromone intensity in real time — brighter purple means more pheromone, revealing how the colony converges.

### Multi-Checkpoint Routing
All four algorithms (BFS, DFS, A*, ACO) support multi-checkpoint routing. Place any number of intermediate waypoints, then click any solver — it automatically breaks the problem into segments (start → checkpoint₁ → checkpoint₂ → ... → end) and solves each segment with your chosen algorithm, stitching them into a complete route.

## Controls

| Button | Action |
|---|---|
| **Generate** | Create a new random maze |
| **Clear** | Reset the entire grid |
| **Restart** | Clear solution paths, keep the maze |
| **Solve by BFS** | Run BFS (direct or through checkpoints) |
| **Solve by DFS** | Run DFS (direct or through checkpoints) |
| **Solve by A\*** | Run A* (direct or through checkpoints) |
| **Solve by ACO** | Run ACO (direct or through checkpoints) |
| **Add checkpoint** | Click to place a waypoint, then click a cell |

**Usage:** After generating a maze, click any open cell to set the **start** (blue), then click another to set the **end** (red). Optionally place checkpoints with **Add checkpoint**. Then click any solver — it routes through all checkpoints automatically.

## Getting Started

```bash
# Clone the repository
git clone https://github.com/JadeEye21/MazeRunner.git
cd MazeRunner

# Install dependencies
pip install pygame numpy

# Run
python MazeTest.py
```

## Configuration

Edit the constants at the top of `MazeTest.py` to customize:

```python
GRIDN = 31      # Grid rows (use odd numbers for clean walls)
GRIDM = 31      # Grid columns
BLOCK_SIZE = 20  # Cell size in pixels
```

## Tech Stack

- **Python 3** — core logic
- **Pygame** — rendering and UI
- **NumPy** — grid state management

## License

MIT
