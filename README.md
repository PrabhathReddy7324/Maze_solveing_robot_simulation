# Maze Solving Robot using Webots

A Python-based maze generator and solver using the Webots robotics simulator. The project creates random mazes and uses an e-puck robot to solve them.

## Project Structure
```
Maze_solving_robot/
├── controllers/
│   ├── mazeSolverController/
│   │   └── mazeSolverController.py    # Robot controller
│   └── supervisor/
│       └── supervisor.py              # Simulation supervisor
├── utils/
│   └── maze_generator.py             # Maze generation script
├── worlds/
│   ├── random_maze.wbt               # Generated maze world
│   └── mazeworld.wbt                 # Template maze world
└── README.md
```

## Features

- Random maze generation using recursive backtracking algorithm
- Configurable maze size and cell dimensions
- Automatic placement of robot at maze entrance
- Clear entrance (bottom-left) and exit (top-right) points
- Integration with Webots simulation environment

## Prerequisites

- Python 3.x
- Webots R2023a or newer
- Required Python packages:
  - `controller` (Webots Python API)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/Maze_solving_robot.git
cd Maze_solving_robot
```

2. Install Webots if you haven't already:
   - Download from [Cyberbotics website](https://cyberbotics.com/)
   - Follow the installation instructions for your platform

## Usage

1. Generate a new random maze:
```bash
python utils/maze_generator.py
```

2. Open Webots and load the generated world:
   - Launch Webots
   - File > Open World...
   - Navigate to `worlds/random_maze.wbt`

3. Start the simulation to watch the robot solve the maze

## Configuration

You can customize the maze generation by modifying parameters in `maze_generator.py`:

```python
# Adjust maze size and cell dimensions
generator = MazeGenerator(
    size=11,        # Number of cells (11x11 grid)
    cell_size=3/11  # Cell size to fit 3x3 floor
)
```

## Development

- The maze generator uses a recursive backtracking algorithm to ensure fully connected paths
- Walls are generated as Webots solid objects with proper physics properties
- Robot starting position is automatically calculated based on the entrance location
