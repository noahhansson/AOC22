import os
from typing import Optional
from copy import deepcopy
from utils import read_input

def get_walls() -> set[tuple[int, int]]:
    inpt = read_input("14")
    inpt_parsed = [[tuple([int(val) for val in coord.split(",")]) for coord in row.split(" -> ")] for row in inpt]
    walls = set()
    for sequence in inpt_parsed:
        s = iter(sequence)
        prev = None
        while (coord := next(s, False)):
            if prev is not None:
                x_0, y_0 = prev
                x_1, y_1 = coord

                if x_0==x_1:
                    for y in range(min(y_0, y_1), max(y_0, y_1) + 1):
                        walls.add((x_0, y))
                elif y_0==y_1:
                    for x in range(min(x_0, x_1), max(x_0, x_1) + 1):
                        walls.add((x, y_0))
            prev = coord

    return walls

def print_grid(walls: set[tuple[int, int]], sand: set[tuple[int, int]]) -> None:
    y_max = max([coord[1] for coord in walls])
    y_min = 0

    x_max = max([coord[0] for coord in walls])
    x_min = min([coord[0] for coord in walls])

    print_grid = [[" . " for _ in range(x_min, x_max + 1)] for _ in range(y_min, y_max + 1)]
    for coord in sand:
        print_grid[coord[1] - y_min][coord[0] - x_min] = "o"
    for coord in walls:
        print_grid[coord[1] - y_min][coord[0] - x_min] = "#"
    print_grid[0][500 - x_min] = "+"

    print("\n".join("".join(row) for row in print_grid))

def get_target(coord: tuple[int, int], walls: set[tuple[int, int]], sand: set[tuple[int, int]]) -> Optional[tuple[int, int]]:
    '''
    Returns the first valid point a grain of sand can fall to, in order of priority
    '''
    for dx, dy in [(0, 1), (-1, 1), (1, 1)]:
        if ((target := (coord[0] + dx, coord[1] + dy)) not in (sand | walls)):
            return target
    return None


def simulate_sand(walls: set[tuple[int, int]]) -> int:
    ymax = max([coord[1] for coord in walls])
    spawn_point = (500, 0)
    sand = set()
    current_sand = deepcopy(spawn_point)

    while True:
        if (target := get_target(current_sand, walls, sand)) is not None:
            current_sand = target
        else:
            #No more space for sand to fall, add it to sand set and spawn a new one
            sand.add((current_sand))
            current_sand = deepcopy(spawn_point)

        if current_sand[1] > ymax:
            return len(sand)

def calculate_sand(walls: set[tuple[int, int]]) -> int:
    spawn_point = (500, 0)
    ymax = max([coord[1] for coord in walls])
    sand = set()
    empty_spaces = set()
    for i, y in enumerate(range(spawn_point[1], ymax + 2)):
        for x in range(spawn_point[0] - i, spawn_point[0] + i + 1):
            if (x,y) not in walls:
                if all([coord in (walls | empty_spaces) for coord in [(x, y-1), (x-1, y-1), (x+1, y-1)]]):
                    empty_spaces.add((x,y))
                else:
                    sand.add((x, y))

    return len((sand - walls) - empty_spaces)

walls = get_walls()
print(simulate_sand(walls=walls))
print(calculate_sand(walls=walls))
