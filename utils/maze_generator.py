import random
import os

class MazeGenerator:
    def __init__(self, size=11, cell_size=3/11):  # 11 cells to fit 3x3 floor
        self.n = size
        self.cell_size = cell_size
        self.v_walls = [[True for _ in range(self.n+1)] for _ in range(self.n)]
        self.h_walls = [[True for _ in range(self.n)] for _ in range(self.n+1)]

    def generate_maze(self):
        # Recursive backtracking
        stack = [(0, 0)]
        visited = [[False for _ in range(self.n)] for _ in range(self.n)]
        visited[0][0] = True

        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.n and 0 <= ny < self.n and not visited[ny][nx]:
                    neighbors.append((nx, ny))
            if neighbors:
                nx, ny = random.choice(neighbors)
                # Remove wall between (x,y) and (nx,ny)
                if nx == x+1:
                    self.v_walls[y][x+1] = False
                elif nx == x-1:
                    self.v_walls[y][x] = False
                elif ny == y+1:
                    self.h_walls[y+1][x] = False
                elif ny == y-1:
                    self.h_walls[y][x] = False
                visited[ny][nx] = True
                stack.append((nx, ny))
            else:
                stack.pop()

        # Openings: entrance (bottom-left), exit (top-right)
        self.h_walls[0][0] = False  # Entrance at bottom-left
        self.h_walls[self.n][self.n-1] = False  # Exit at top-right

        # Generate wall objects
        walls = []
        offset = -1.5 + self.cell_size / 2
        wall_thickness = 0.01
        wall_height = 0.1

        # Vertical walls
        for y in range(self.n):
            for x in range(self.n+1):
                if self.v_walls[y][x]:
                    wx = offset + (x-0.5)*self.cell_size
                    wz = offset + y*self.cell_size
                    walls.append(f"""
DEF WALL_V_{x}_{y} Solid {{
  translation {wx} {wall_height/2} {wz}
  children [
    Shape {{
      appearance Appearance {{
        material Material {{
          diffuseColor 0.2 0.5 0.4
        }}
      }}
      geometry Box {{
        size {wall_thickness} {wall_height} {self.cell_size}
      }}
    }}
  ]
  boundingObject Box {{
    size {wall_thickness} {wall_height} {self.cell_size}
  }}
}}""")
        # Horizontal walls
        for y in range(self.n+1):
            for x in range(self.n):
                if self.h_walls[y][x]:
                    wx = offset + x*self.cell_size
                    wz = offset + (y-0.5)*self.cell_size
                    walls.append(f"""
DEF WALL_H_{x}_{y} Solid {{
  translation {wx} {wall_height/2} {wz}
  children [
    Shape {{
      appearance Appearance {{
        material Material {{
          diffuseColor 0.2 0.5 0.4
        }}
      }}
      geometry Box {{
        size {self.cell_size} {wall_height} {wall_thickness}
      }}
    }}
  ]
  boundingObject Box {{
    size {self.cell_size} {wall_height} {wall_thickness}
  }}
}}""")
        return walls

def modify_world_file(walls):
    world_template = """#VRML_SIM R2025a utf8

EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/projects/robots/gctronic/e-puck/protos/E-puck.proto"
EXTERNPROTO "https://raw.githubusercontent.com/cyberbotics/webots/R2025a/projects/objects/floors/protos/Floor.proto"

WorldInfo {{
  basicTimeStep 16
  coordinateSystem "NUE"
}}
Viewpoint {{
  orientation -0.9296751396558008 0.20052478374983415 -0.3090209471994569 1.612703378081761
  position -2.1950198024239507 0.703279700537823 1.076312388314976
}}
Background {{
  skyColor [
    0.4 0.7 1
  ]
}}
DirectionalLight {{
  ambientIntensity 1
  direction 0 -1 0
  intensity 0.2
  castShadows TRUE
}}
Floor {{
  rotation -1 0 0 1.5707903061004251
  size 3 3
  texture [
    "textures/steel_floor.jpg"
  ]
}}
{walls}
E-puck {{
  translation -1.44993 -5.69147e-05 -1.28975
  rotation -0.5773502691896258 0.5773502691896258 0.5773502691896258 2.0944
  name "e-puck"
  controller "mazeSolverController"
  version "2"
  camera_width 160
  camera_height 120
  emitter_channel 3
  receiver_channel 4
  turretSlot [
    GPS {{
    }}
  ]
}}"""

    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    worlds_dir = os.path.join(project_root, 'worlds')
    os.makedirs(worlds_dir, exist_ok=True)
    output_file = os.path.join(worlds_dir, 'random_maze.wbt')
    walls_str = "\n".join(walls)
    with open(output_file, "w") as f:
        f.write(world_template.format(walls=walls_str))
    print(f"Maze generated at: {output_file}")

if __name__ == "__main__":
    try:
        generator = MazeGenerator(size=11, cell_size=3/11)
        walls = generator.generate_maze()
        if not walls:
            print("No walls were generated!")
            exit(1)
        modify_world_file(walls)
        print(f"Generated {len(walls)} walls successfully!")
    except Exception as e:
        print(f"Error generating maze: {str(e)}")