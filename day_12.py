from heapq import heapify, heappop, heappush
from utils import read_input

inpt = read_input("12")

grid = [[x for x in row] for row in inpt]



def get_neighbours(point: tuple[int, int]) -> set[tuple[int, int]]:
    neighbours = set()
    for step in ((0,1), (0,-1), (1,0), (-1,0)):
        if (point[0] + step[0]) < 0 or (point[0] + step[0]) >= len(grid):
            # X out of bounds
            continue
        elif (point[1] + step[1]) < 0 or (point[1] + step[1]) >= len(grid[0]):
            # Y out of bounds
            continue
        else:
            neighbours.add((point[0] + step[0], point[1] + step[1]))
    return neighbours

def find_point(grid: list[list[str]], value: str):
    for i, row in enumerate(grid):
        for j, height in enumerate(row):
            if height == value:
                return (i, j)

def search(start: tuple[int, int], grid: list[list[str]], target: str, part_2: bool=False) -> int:

    letters = sorted(list(set("the quick brown fox jumps over the lazy dog".replace(" ", ""))))
    scores = {letter: i + 1 for i, letter in enumerate(letters)}
    scores["S"] = scores["a"]
    scores["E"] = scores["z"]

    visited = set()
    dist = 0
    heap = [(dist, start)]
    heapify(heap)
    visited.add(start)

    while (item := heappop(heap)):
        dist, node = item
        if grid[node[0]][node[1]] == target:
            return dist
        height = scores[grid[node[0]][node[1]]]
        for neighbour in get_neighbours(node):
            height_diff = scores[grid[neighbour[0]][neighbour[1]]] - height
            if (
                #Check if neighbouring node is within height requirement
                ((part_2 and height_diff >= -1) or ((not part_2) and (height_diff <= 1))) and 
                #Check if node is already visited
                (neighbour not in visited)
            ):
                visited.add(neighbour)
                heappush(heap, (dist + 1, neighbour))

def get_first_solution():
    return search(find_point(grid, "S"), grid, "E")

def get_second_solution():
    return search(find_point(grid, "E"), grid, "a", part_2=True)

print(get_first_solution())
print(get_second_solution())
