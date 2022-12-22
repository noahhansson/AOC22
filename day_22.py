import os
from enum import Enum

def read_input(file_name:str) -> str:
    input_file = os.path.join(os.getcwd(), "input", f"{file_name}.txt")
    with open(input_file, 'r') as file:
        contents = [val.strip("\n") for val in file.readlines()]
    return contents

class Directions(Enum):
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
    direction = Directions.RIGHT

    for instruction in instructions:
        match instruction:
            case int():
                for step in range(instruction):

                    #Move in the right direction
                    if direction == Directions.RIGHT:
                        new_position = (position[0] + 1, position[1])
                    elif direction == Directions.DOWN:
                        new_position = (position[0], position[1] + 1)
                    elif direction == Directions.LEFT:
                        new_position = (position[0] - 1, position[1])
                    elif direction == Directions.UP:
                        new_position = (position[0], position[1] - 1)

                    if direction in (Directions.LEFT, Directions.RIGHT):
                        #Check for looping in x
                        x, y = new_position
                        row_edges = edges[y]
                        if x == row_edges[0]:
                            new_position = (row_edges[1] - 1, y)
                        elif x == row_edges[1]:
                            new_position = (row_edges[0] + 1, y)

                    elif direction in (Directions.UP, Directions.DOWN):
                        #Check for looping in y
                        x, y = new_position

                        if (y == len(edges)) or (x <= edges[y][0]) or (x >= edges[y][1]):
                            if direction == Directions.DOWN:
                                #Search upwards for last point thas is not out
                                #of bounds
                                while True:
                                    if y <= 0:
                                        break
                                    row_edges = edges[y - 1]
                                    if (x <= row_edges[0]) or (x >= row_edges[1]):
                                        break
                                    y -= 1

                            elif direction == Directions.UP:
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
                direction = Directions((direction.value + 1)%4)
            case 'L':
                #rotate left
                direction = Directions((direction.value - 1)%4)
    
    return 1000 * (position[1] + 1) + 4 * (position[0] + 1) + direction.value

def get_second_solution():
    pass

print(get_first_solution())
print(get_second_solution())