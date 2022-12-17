from utils import read_input
from itertools import cycle
from functools import cache
from time import sleep

inpt = read_input("17")
inpt_parsed = [c for c in inpt[0]]

rocks = [
    [(0, 0), (1, 0), (2, 0), (3, 0)], #Horizontal line
    [(0, 1), (1, 1), (2, 1), (1, 2), (1, 0)], #Plus
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], #Reverse L
    [(0, 0), (0, 1), (0, 2), (0, 3)], #Vertical line
    [(0, 0), (1, 0), (0, 1), (1, 1)] #Square
]

def draw_rocks(settled_rocks: set[tuple[int, int]], falling_rocks: set[tuple[int, int]] = set()):

    max_y = max([y for _, y in settled_rocks | falling_rocks])

    grid = [["." for x in range(7)] for y in range(max_y + 1)]
    for point in settled_rocks:
        grid[max_y - point[1]][point[0]] = "#"
    for point in falling_rocks:
        grid[max_y - point[1]][point[0]] = "@"

    print("\n".join(["".join(row) for row in grid]) + "\n")
    with open("draw.txt", "w+") as outfile:
        outfile.write("\n".join(["".join(row) for row in grid]))


rock_cache = {}

def drop_rock(
    settled_rocks: frozenset[tuple[int, int]], 
    rock_type: int, 
    jet_index: int
) -> tuple[list[tuple[int, int]], int]:

    key = hash(settled_rocks) + hash(rock_type) + hash(jet_index)
    if key in rock_cache.keys():
        #print(f"Returned cached value for rock type {rock_type}, jet index {jet_index}")
        return rock_cache[key]

    '''
    Calculates the final position of a falling rock given the current
    wind, the rock type and the rocks on the ground
    '''
    #Create the rock
    if settled_rocks:
        max_y = max([y for _, y in settled_rocks])
    else:
        max_y = -1
    start_position = (2, max_y + 4)
    rock = [
        (x + start_position[0], y + start_position[1]) 
        for x, y in rocks[rock_type]
    ]

    i = jet_index

    while True:

        step = inpt_parsed[i]
        i = (i + 1)%len(inpt_parsed)

        #Logic for updatimg position of falling rock
        #First push left/right
        match step:
            case '>':
                moved_rock = [(x + 1, y) for x, y in rock]
            case '<':
                moved_rock = [(x - 1, y) for x, y in rock]
        if not (
            any([point in settled_rocks for point in moved_rock]) or
            any([x>=7 or x<0 for x, _ in moved_rock])   
            
        ):
            #Rock can move left or right due to no collison with settled rock or wall
            rock = moved_rock

        #Then move down, settling if reaching the floor or any other rock
        moved_rock = [(x, y - 1) for x, y in rock]
        if (
            any([point in settled_rocks for point in moved_rock]) or
            any([y<0 for _, y in moved_rock])
        ):
            #Rock has collided, do not move and add all points to settled rocks
            rock_cache[key] = (rock, i)
            #print(f"Cached value for rock type {rock_type}, jet index {jet_index}")
            return rock, i

        rock = moved_rock


def solve(n_rocks: int):

    rock_idx = 0
    settled_rocks = frozenset()
    jet_idx = 0
    total_height = 0

    while True:
        if (rock_idx % 5000 == 0) and (rock_idx != 0):
            #draw_rocks(settled_rocks)
            print(rock_idx)

        if rock_idx == (n_rocks):
            return total_height + max([y for _, y in settled_rocks]) + 1

        n = 30
        if settled_rocks:
            max_y = max([y for _, y in settled_rocks])
        else:
            max_y = 0

        if max_y > n:
            min_y = max_y - n
            total_height += min_y
            settled_rocks = frozenset((x, y - min_y) for x, y in settled_rocks if y > min_y)

        rock_type = rock_idx % len(rocks)
        #Create a set of the top n rows of settled rocks
        settled_rock, jet_idx = drop_rock(
                                    settled_rocks, 
                                    rock_type,
                                    jet_idx)

        settled_rocks = frozenset(rock for rock in settled_rocks | frozenset(settled_rock))

        #draw_rocks(settled_rocks=settled_rocks)
        #sleep(2)

        rock_idx += 1

def get_first_solution():
    return solve(2022)

def get_second_solution():
    return solve(1000000000000)

print(get_first_solution())
#print(get_second_solution())