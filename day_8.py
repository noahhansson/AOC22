from utils import read_input

inpt = read_input("8")
inpt_parsed = [[int(x) for x in row] for row in inpt]

def get_first_solution():
    shape = (len(inpt_parsed[0]), len(inpt_parsed))
    vision = [[0 for _ in range(shape[1])] for _ in range(shape[0])]

    #Left to right
    for i, row in enumerate(inpt_parsed):
        max_height = -1
        for j, height in enumerate(row):
            #print(f"({i}, {j}), Height {height}, current max: {max_height}")
            if height > max_height:
                max_height = height
                vision[i][j] = 1
    #Right to left
    for i, row in enumerate(inpt_parsed):
        max_height = -1
        for j, height in enumerate(reversed(row)):
            #print(f"({i}, {shape[1]-j-1}), Height {height}, current max: {max_height}")
            if height > max_height:
                max_height = height
                vision[i][shape[1]-j-1] = 1
    #Up to Down
    for j in range(shape[1]):
        max_height = -1
        for i in range(shape[0]):
            height = inpt_parsed[i][j]
            #print(f"({i}, {j}), Height {height}, current max: {max_height}")
            if height > max_height:
                max_height = height
                vision[i][j] = 1
    #Down to up
    for j in range(shape[1]):
        max_height = -1
        for i in range(shape[0]):
            height = inpt_parsed[shape[0]-i-1][j]
            #print(f"({shape[0]-i}, {j}), Height {height}, current max: {max_height}")
            if height > max_height:
                max_height = height
                vision[shape[0]-i-1][j] = 1

    return sum([sum(row) for row in vision])

def get_second_solution():
    def vision(grid: list[list[int]], starting_point: tuple[int, int], direction: tuple[int, int]) -> int:
        shape = (len(grid[0]), len(grid))
        i, j = starting_point
        current_height = grid[i][j]
        vision = 0
        while True:
            #Take one step
            i += direction[0]
            j += direction[1]

            if (i < 0 or i >= shape[0]) or j < 0 or j >= shape[1]:
                break

            height = grid[i][j]
            if height < current_height:
                vision += 1
            elif height >= current_height:
                vision += 1
                break
            else:
                break

        return vision

    shape = (len(inpt_parsed[0]), len(inpt_parsed))
    scores = [[0 for _ in range(shape[1])] for _ in range(shape[0])]
    for i in range(shape[0]):
        for j in range(shape[1]):
            up = vision(inpt_parsed, (i, j), (-1, 0))
            down = vision(inpt_parsed, (i, j), (1, 0))
            left = vision(inpt_parsed, (i, j), (0, -1))
            right = vision(inpt_parsed, (i, j), (0, 1))
            scores[i][j] =  up*down*left*right
            #print(f"({i}, {j}), Scores: up {up}, down {down}, left {left} right {right}, Total: {scores[i][j]}")

    return max([max(score) for score in scores])


print(get_first_solution())
print(get_second_solution())
