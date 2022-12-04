from utils import read_input

inpt = read_input("3")

letters_lower = sorted(list(set("the quick brown fox jumps over the lazy dog".replace(" ", ""))))
letters_upper = sorted(list(set("the quick brown fox jumps over the lazy dog".replace(" ", "").upper())))

letters = letters_lower + letters_upper

priority = {
    letter: i+1 for i, letter in enumerate(letters)
}

def get_first_solution():

    inpt_parsed = [
        (set(contents[:len(contents)//2]), set(contents[len(contents)//2:]))
        for contents in inpt 
    ]

    overlap_sum = 0
    for rucksack in inpt_parsed:
        overlap = rucksack[0].intersection(rucksack[1])
        overlap_sum += sum([priority[item] for item in overlap])

    return overlap_sum

def get_second_solution():

    inpt_parsed = [
        (set(inpt[i]), set(inpt[i+1]), set(inpt[i+2]))
        for i in range(0, len(inpt), 3) 
    ]

    overlap_sum = 0
    for grp in inpt_parsed:
        overlap = grp[0].intersection(grp[1]).intersection(grp[2])
        overlap_sum += sum([priority[item] for item in overlap])

    return overlap_sum



print(get_first_solution())
print(get_second_solution())