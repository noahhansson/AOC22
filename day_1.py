from utils import read_input

inpt = read_input("1")


def get_first_solution():
    max_cal = 0

    current_cal = 0
    for val in inpt:
        if val != '':
            current_cal += int(val)

        if current_cal > max_cal:
            max_cal = current_cal

        if val == '':
            current_cal = 0

    return max_cal

def get_second_solution():
    cal_list = []
    elf_idx = 0
    current_cal = 0
    for val in inpt:
        if val != '':
            current_cal += int(val)

        if val == '':
            cal_list.append(current_cal)
            elf_idx += 1
            current_cal = 0

    return sum(sorted(cal_list)[-3:])



print(get_first_solution())
print(get_second_solution())