from utils import read_input
from typing import Iterable, Optional
from time import sleep
import os

inpt = read_input("18")
inpt_parsed = [tuple([int(x) for x in cube.split(",")]) for cube in inpt]

def neighbour_3d(p: tuple[int, int, int]) -> list[tuple[int, int, int]]:
    x, y, z = p
    return [
        (x + 1, y, z),
        (x - 1, y, z),
        (x, y + 1, z),
        (x, y - 1, z),
        (x, y, z + 1),
        (x, y, z - 1)
    ]

def print_slice(
    cubes: Iterable[tuple[int, int, int]],
    outside_cubes: set(tuple[int, int, int]) = set(),
    x: Optional[int] = None, 
    y: Optional[int] = None, 
    z: Optional[int] = None
) -> None:
    x_min = min([x for x, _, _ in cubes])
    x_max = max([x for x, _, _ in cubes])
    y_min = min([y for _, y, _ in cubes])
    y_max = max([y for _, y, _ in cubes])
    z_min = min([z for _, _, z in cubes])
    z_max = max([z for _, _, z in cubes])

    grid = []

    def _helper(x, y, z):
        if (x, y, z) in cubes:
            return "#"
        elif (x, y, z) in outside_cubes:
            return "~"
        else:
            return "."

    if x is not None:
        #Fixate x
        grid = [[_helper(x, y, z) for y in range(y_min, y_max + 1)] for z in range(z_min, z_max + 1)]
    elif y is not None:
        #Fixate y
        grid = [[_helper(x, y, z) for x in range(x_min, x_max + 1)] for z in range(z_min, z_max + 1)]

    elif z is not None:
        #Fixate z
        grid = [[_helper(x, y, z) for x in range(x_min, x_max + 1)] for y in range(y_min, y_max + 1)]

    print("\n".join(" ".join(row) for row in grid))


def get_first_solution():

    return sum(
        [sum([s not in inpt_parsed]) 
        for cube in inpt_parsed 
        for s in neighbour_3d(cube)]
    )

def get_second_solution():

    x_min = min([x for x, _, _ in inpt_parsed])
    x_max = max([x for x, _, _ in inpt_parsed])
    y_min = min([y for _, y, _ in inpt_parsed])
    y_max = max([y for _, y, _ in inpt_parsed])
    z_min = min([z for _, _, z in inpt_parsed])
    z_max = max([z for _, _, z in inpt_parsed])

    outside_cubes = set()
    queue = []
    queue.append(((10, 10, -1)))

    while queue:
        side = queue.pop()
        for neighbour in neighbour_3d(side):
            if (
                ((x_min - 1) <= neighbour[0] <= (x_max + 1)) and
                ((y_min - 1) <= neighbour[1] <= (y_max + 1)) and
                ((z_min - 1) <= neighbour[2] <= (z_max + 1))
            ):
                if (
                    (neighbour not in inpt_parsed) and 
                    (neighbour not in outside_cubes)   
                ):
                    queue.append(neighbour)
        outside_cubes.add(side)


    #Print a cool animation
    for x in range(x_min - 1, x_max + 2):
        os.system('cls')
        print_slice(inpt_parsed, outside_cubes, x=x)
        sleep(0.05)

    for y in range(y_min - 1, y_max + 2):
        os.system('cls')
        print_slice(inpt_parsed, outside_cubes, y=y)
        sleep(0.05)

    for z in range(z_min - 1, z_max + 2):
        os.system('cls')
        print_slice(inpt_parsed, outside_cubes, z=z)
        sleep(0.05)

    os.system('cls')

    return sum(
        [sum([(s not in inpt_parsed) and (s in outside_cubes)]) 
        for cube in inpt_parsed 
        for s in neighbour_3d(cube)]
    )

print(get_first_solution())
print(get_second_solution())