from utils import read_input

inpt = read_input("6")[0]

def get_first_solution():
    for i in range(len(inpt)):
        if i>4:
            if len(set(inpt[i-4:i])) == 4:
                return i

def get_second_solution():
    for i in range(len(inpt)):
        if i>14:
            if len(set(inpt[i-14:i])) == 14:
                return i

print(get_first_solution())
print(get_second_solution())