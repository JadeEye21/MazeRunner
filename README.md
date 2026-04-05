# MazeRunner

An interactive maze generator and pathfinding visualizer built with Python and Pygame. Generate random mazes and watch BFS and DFS algorithms solve them in real time.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)

## Features

- **Randomized Maze Generation** — Prim's algorithm variant that carves paths through a grid, producing unique solvable mazes every run
- **BFS Solver** — Breadth-first search with wave-propagation visualization; guarantees the shortest path
- **DFS Solver** — Depth-first search with backtracking; explores paths exhaustively and highlights the solution
- **Checkpoint Routing** — Place intermediate waypoints and compute a multi-segment route through all of them in order
- **Real-time Animation** — Watch each algorithm explore the maze cell by cell, with color-coded states:
  - ⬜ White — open path
  - ⬛ Black — wall
  - 🟦 Blue — start / solution path
  - 🟥 Red — end
  - 🟩 Green — checkpoint
  - 🟨 Yellow — visited (DFS exploration)

## How It Works

### Maze Generation
The generator starts from a seed cell and uses a randomized variant of Prim's algorithm. It maintains a frontier of candidate cells, randomly selects one, carves a passage to an adjacent visited cell, and repeats until every cell is reachable.

### BFS (Breadth-First Search)
Explores all neighbors at the current depth before moving deeper. Uses a wavefront that expands outward from the start, guaranteeing the shortest path. Each cell stores its distance, and the path is reconstructed by tracing back from the end.

### DFS (Depth-First Search)
Uses a stack to explore as deep as possible along each branch before backtracking. Visited dead-ends are marked and skipped. The final path is the stack contents when the end is reached.

### Checkpoint Routing
When checkpoints are placed, the solver runs DFS between consecutive waypoints (start → checkpoint₁ → checkpoint₂ → ... → end) and stitches the segments together into a complete route.

## Controls

| Button | Action |
|---|---|
| **Generate** | Create a new random maze |
| **Clear** | Reset the entire grid |
| **Restart** | Clear solution paths, keep the maze |
| **Solve by BFS** | Run BFS from start to end |
| **Solve by DFS** | Run DFS from start to end |
| **Add checkpoint** | Click to place a waypoint, then click a cell |
| **Route** | Solve through all checkpoints |

**Usage:** After generating a maze, click any open cell to set the **start** (blue), then click another to set the **end** (red). Then choose a solver.

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
blockSize = 20   # Cell size in pixels
```

## Tech Stack

- **Python 3** — core logic
- **Pygame** — rendering and UI
- **NumPy** — grid state management

## License

MIT
