from utils import read_input

blizzard_type = set[tuple[tuple[int, int], str]]

def get_grid() -> tuple[blizzard_type, tuple[int, int]]:
    inpt = read_input("24")
    #Ignore walls
    grid_size = (len(inpt[0]) - 2, len(inpt) - 2)
    blizzards = set()

    for y, row in enumerate(inpt):
        for x, char in enumerate(row):
            if char in {"<", ">", "^", "v"}:
                blizzards.add(((x - 1, y - 1), char))

    return blizzards, grid_size

def move_blizzards(
    blizzards: blizzard_type, 
    grid_size: tuple[int, int]
) -> blizzard_type:

    new_blizzards = set()
    for blizzard in blizzards:
        position, direction = blizzard
        match direction:
            case "^":
                new_position = (position[0], (position[1] - 1)%(grid_size[1]))
            case "v":
                new_position = (position[0], (position[1] + 1)%(grid_size[1]))
            case "<":
                new_position = ((position[0] - 1)%(grid_size[0]), position[1])
            case ">":
                new_position = ((position[0] + 1)%(grid_size[0]), position[1])
        new_blizzards.add((new_position, direction))

    return new_blizzards

def get_neighbours(
    position: tuple[int, int], 
    blizzards: blizzard_type, 
    grid_size: tuple[int, int]
    ) -> set[tuple[int, int]]:

    moves = {
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (0, 0)
    }

    blizzard_positions = {blizzard[0] for blizzard in blizzards}
    next_positions = set()

    for move in moves:
        next_position = (position[0] + move[0], position[1] + move[1])
        if (
            next_position not in blizzard_positions 
            and (
                ((0 <= next_position[0] < grid_size[0]) and (0 <= next_position[1] < grid_size[1])) 
                or next_position == (0, -1) 
                or next_position == (grid_size[0] - 1, grid_size[1])
            )
        ):
            next_positions.add(next_position)

    return next_positions

def traverse_snowstorm(
    start: tuple[int, int], 
    end: tuple[int, int], 
    blizzards: blizzard_type, 
    grid_size: tuple[int, int]
    ) -> tuple[int, blizzard_type]:

    #BFS
    positions = set()
    positions.add(start)

    i = 0
    while True:
        if end in positions:
            return i, blizzards
        blizzards = move_blizzards(blizzards, grid_size)
        next_positions = set()
        for position in positions:
            for neighbour in get_neighbours(position, blizzards, grid_size):
                next_positions.add(neighbour)
        
        positions = next_positions
        i+=1

def get_first_solution() -> int:
    blizzards, grid_size = get_grid()
    start = (0, -1)
    end = (grid_size[0] - 1, grid_size[1])
    return traverse_snowstorm(start, end, blizzards, grid_size)[0]
        

def get_second_solution() -> int:
    blizzards, grid_size = get_grid()
    start = (0, -1)
    end = (grid_size[0] - 1, grid_size[1])

    t1, blizzards = traverse_snowstorm(start, end, blizzards, grid_size)
    t2, blizzards = traverse_snowstorm(end, start, blizzards, grid_size)
    t3, blizzards = traverse_snowstorm(start, end, blizzards, grid_size)

    return t1+t2+t3



print(get_first_solution())
print(get_second_solution())