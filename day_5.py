from utils import read_input
from copy import deepcopy

inpt = read_input("5")

crates, instructions = inpt[:8], inpt[10:]

crates = crates[::-1]
crates = [level.replace("[", "").replace("] ", "").replace("]", "").replace("   ", "") for level in crates]
piles = [[] for _ in range(len(crates[0]))]
for i, level in enumerate(crates):
    for j, item in enumerate(level):
        if item != " ":
            piles[j].append(item)

instructions = [eval("(" + instruction.replace("move ", "").replace(" from ", ",").replace(" to ", ",") + ")") for instruction in instructions]

def get_first_solution():
    piles_1 = deepcopy(piles)
    for q, frm, to  in instructions:
        for _ in range(q):
            piles_1[to-1].append(piles_1[frm-1].pop())

    return "".join([pile[-1] for pile in piles_1])

def get_second_solution():
    piles_2 = deepcopy(piles)
    for q, frm, to  in instructions:
        piles_2[to-1] += piles_2[frm-1][-q:]
        del piles_2[frm-1][-q:]

    return "".join([pile[-1] for pile in piles_2])

print(get_first_solution())
print(get_second_solution())