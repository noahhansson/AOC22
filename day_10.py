from utils import read_input

inpt = read_input("10")

current = 1
signal = []
for instruction in inpt:
    match instruction.split(" "):
        case ["noop"]:
            signal += [current]
        case ["addx", number]:
            signal += [current, current]
            current += int(number)

def get_first_solution():
    signal_sum = 0
    for i in (20, 60, 100, 140, 180, 220):
        value = signal[i - 1]
        signal_sum += value * i

    return signal_sum

def get_second_solution():
    crt = [["." for _ in range(40)] for _ in range(6)]

    cycle = 1
    for j in range(6):
        for i in range(40):
            if signal[cycle - 1] in (i-1, i, i+1):
                crt[j][i] = "#"
            cycle += 1
    return "\n".join(" ".join(row) for row in crt)

print(get_first_solution())
print(get_second_solution())