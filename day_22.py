import os
from typing import Self
from enum import Enum

def read_input(file_name:str) -> str:
    input_file = os.path.join(os.getcwd(), "input", f"{file_name}.txt")
    with open(input_file, 'r') as file:
        contents = [val.strip("\n") for val in file.readlines()]
    return contents

class Direction(Enum):
    RIGHT=0
    DOWN=1
    LEFT=2
    UP=3

def read_map() -> tuple[set[tuple[int, int]], list[tuple[int, int]], list[int | str]]:
    inpt = read_input("22")
    monkey_map = inpt[:-2]
    instructions = inpt[-1]
    edges = []
    walls = set()
    for i, row in enumerate(monkey_map):
        #Parse map edges
        map_start = 0
        for c in row:
            if c != " ":
                break
            else:
                map_start += 1
        map_end = len(row)
        edges.append((map_start-1, map_end))
        #Parse walls
        for j, c in enumerate(row):
            if c == "#":
                walls.add((j, i))

    instructions = instructions.replace("R", ",R,").replace("L", ",L,").split(",")
    instructions = [int(x) if x not in ("R", "L") else x for x in instructions]

    return walls, edges, instructions


def get_first_solution():
    walls, edges, instructions = read_map()
    start_row = 0

    position = (edges[start_row][0] + 1, start_row)
    direction = Direction.RIGHT

    for instruction in instructions:
        match instruction:
            case int():
                for step in range(instruction):

                    #Move in the right direction
                    if direction == Direction.RIGHT:
                        new_position = (position[0] + 1, position[1])
                    elif direction == Direction.DOWN:
                        new_position = (position[0], position[1] + 1)
                    elif direction == Direction.LEFT:
                        new_position = (position[0] - 1, position[1])
                    elif direction == Direction.UP:
                        new_position = (position[0], position[1] - 1)

                    if direction in (Direction.LEFT, Direction.RIGHT):
                        #Check for looping in x
                        x, y = new_position
                        row_edges = edges[y]
                        if x == row_edges[0]:
                            new_position = (row_edges[1] - 1, y)
                        elif x == row_edges[1]:
                            new_position = (row_edges[0] + 1, y)

                    elif direction in (Direction.UP, Direction.DOWN):
                        #Check for looping in y
                        x, y = new_position

                        if (y == len(edges)) or (x <= edges[y][0]) or (x >= edges[y][1]):
                            if direction == Direction.DOWN:
                                #Search upwards for last point thas is not out
                                #of bounds
                                while True:
                                    if y <= 0:
                                        break
                                    row_edges = edges[y - 1]
                                    if (x <= row_edges[0]) or (x >= row_edges[1]):
                                        break
                                    y -= 1

                            elif direction == Direction.UP:
                                while True:
                                    if y >= (len(edges) - 1):
                                        break
                                    row_edges = edges[y + 1]
                                    if (x <= row_edges[0]) or (x >= row_edges[1]):
                                        break
                                    y += 1

                        new_position = (x, y)

                    #Check for colission
                    if new_position in walls:
                        break
                    else:
                        position = new_position

            case 'R':
                #rotate right
                direction = Direction((direction.value + 1)%4)
            case 'L':
                #rotate left
                direction = Direction((direction.value - 1)%4)
    
    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + direction.value

def get_face(point: tuple[int, int]) -> int:
    x, y = point

    if (50 <= x < 100) and (0 <= y < 50):
        return 1
    elif (100 <= x < 150) and (0 <= y < 50):
        return 2
    elif (50 <= x < 100) and (50 <= y < 100):
        return 3
    elif (50 <= x < 100) and (100 <= y < 150):
        return 4
    elif (0 <= x < 50) and (100 <= y < 150):
        return 5
    elif (0 <= x < 50) and (150 <= y < 200):
        return 6
    else:
        return 0

def traverse(current_point: tuple[int, int], direction: Direction) -> tuple[tuple[int, int], Direction]:

    x, y = current_point
    if direction == Direction.UP:
        next_point = (x, y-1)
    elif direction == Direction.RIGHT:
        next_point = (x+1, y)
    elif direction == Direction.DOWN:
        next_point = (x, y+1)
    elif direction == Direction.LEFT:
        next_point = (x-1, y)

    if get_face(next_point)==get_face(current_point):
        return next_point, direction

    else:

        x = x % 50
        y = y % 50

        match (get_face(current_point), direction):
            case (1, Direction.RIGHT):
                next_direction = direction

            case (1, Direction.DOWN):
                next_direction = direction

            case (1, Direction.LEFT):
                next_point = (0, 149 - y)
                next_direction = Direction.RIGHT

            case (1, Direction.UP):
                next_point = (0, 150 + x)
                next_direction = Direction.RIGHT

            case (2, Direction.LEFT):
                next_direction = direction
            
            case (2, Direction.DOWN):
                next_point = (99, x + 50)
                next_direction = Direction.LEFT
            
            case (2, Direction.RIGHT):
                next_point = (99, 149 - y)
                next_direction = Direction.LEFT
            
            case (2, Direction.UP):
                next_point = (x, 199)
                next_direction = Direction.UP
            
            case (3, Direction.UP):
                next_direction = direction
            
            case (3, Direction.RIGHT):
                next_point = ((y + 100), 49)
                next_direction = Direction.UP
            
            case (3, Direction.LEFT):
                next_point = (y, 100)
                next_direction = Direction.DOWN
            
            case (3, Direction.DOWN):
                next_direction = direction
            
            case (4, Direction.RIGHT):
                next_point = (149, (49 - y))
                next_direction = Direction.LEFT
            
            case (4, Direction.UP):
                next_direction = direction
            
            case (4, Direction.LEFT):
                next_direction = direction
            
            case (4, Direction.DOWN):
                next_point = (49, (150 + x))
                next_direction = Direction.LEFT
            
            case (5, Direction.LEFT):
                next_point = (50, (49 - y))
                next_direction = Direction.RIGHT
            
            case (5, Direction.UP):
                next_point = (50, x + 50)
                next_direction = Direction.RIGHT
            
            case (5, Direction.RIGHT):
                next_direction = direction
            
            case (5, Direction.DOWN):
                next_direction = direction
            
            case (6, Direction.LEFT):
                next_point = ((y + 50), 0)
                next_direction = Direction.DOWN
            
            case (6, Direction.DOWN):
                next_point = ((100 + x), 0)
                next_direction = Direction.DOWN
            
            case (6, Direction.RIGHT):
                next_point = ((y + 50), 149)
                next_direction = Direction.UP
            
            case (6, Direction.UP):
                next_direction = direction
            

        return next_point, next_direction

def print_map(walls, been):
    grid = [["." if get_face((x, y)) > 0 else " " for x in range(0, 150)] for y in range(0, 200)]
    for x, y in walls:
        grid[y][x] = "#"
    for (x, y), direction in been.items():
        if direction == Direction.UP:
            grid[y][x] = "^"
        elif direction == Direction.LEFT:
            grid[y][x] = "<"
        elif direction == Direction.RIGHT:
            grid[y][x] = ">"
        elif direction == Direction.DOWN:
            grid[y][x] = "v"
    print("\n".join([" ".join(row) for row in grid]))


def get_second_solution():
    walls, _, instructions = read_map()

    position = (50, 0)
    direction = Direction.RIGHT

    been = {}
    been[position] = direction

    for instruction in instructions:
        match instruction:
            case int():
                for step in range(instruction):
                    new_position, new_direction = traverse(position, direction)

                    #Check for colission
                    if new_position in walls:
                        break
                    else:
                        position = new_position
                        direction = new_direction

                    been[position] = direction

            case 'R':
                #rotate right
                direction = Direction((direction.value + 1)%4)
            case 'L':
                #rotate left
                direction = Direction((direction.value - 1)%4)

    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + direction.value

print(get_first_solution())
print(get_second_solution())