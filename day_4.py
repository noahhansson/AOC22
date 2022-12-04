from utils import read_input

inpt = read_input("4")
inpt_parsed = [[[int(x) for x in ids.split("-")] for ids in pair.split(",")] for pair in inpt]

def get_first_solution():
    count=0
    for pair in inpt_parsed:
        #Two cases: left is contained in right or right is contained in left.
        #Check that the greater pair has a greater end and smaller start for
        #both cases
        if (
            (pair[0][0] <= pair[1][0] and pair[0][1] >= pair[1][1]) 
            or (pair[0][0] >= pair[1][0] and pair[0][1] <= pair[1][1])
        ):
            count+=1
    return count

def get_second_solution():
    count=0
    for pair in inpt_parsed:
        #Only one case: Check if the end of left is greater than the start of
        #right and that the start of left is lesser than the end of right
        if (pair[0][1] >= pair[1][0] and pair[0][0] <= pair[1][1]):
            count+=1
    return count



print(get_first_solution())
print(get_second_solution())