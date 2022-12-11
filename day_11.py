from utils import read_input
from copy import deepcopy

inpt = read_input("11")
inpt_parsed = []
for line in inpt + [""]:
    match line.split(" "):
        case ["Monkey", i]:
            idx = i
            current = {}
        case ["Starting", "items:", *items]:
            current["items"] = [int(item.strip(",")) for item in items]
        case ["Operation:", *operation]:
            current["operation"] = " ".join(operation)
        case ["Test:", *test]:
            current["test"] = int(test[-1])
        case ["If", "true:", *other]:
            current["true"] = int(other[-1])
        case ["If", "false:", *other]:
            current["false"] = int(other[-1])
            current["monkey business"] = 0
            inpt_parsed.append(current)
            


def get_first_solution():
    monkeys = deepcopy(inpt_parsed)
    for j in range(20):
        for i, monkey in enumerate(monkeys):
            while monkey["items"]:
                item = monkey["items"].pop()
                operation = monkey["operation"].split("=")[-1].strip()
                match operation.split(" "):
                    case ["old", "*", "old"]:
                        new = item*item
                    case ["old", "*", i]:
                        new = item * int(i)
                    case ["old", "+", i]:
                        new = item + int(i)
                new = new // 3
                if new % monkey["test"] == 0:
                    next_monkey = monkey["true"]
                    monkeys[next_monkey]["items"].append(new)
                else:
                    next_monkey = monkey["false"]
                    monkeys[next_monkey]["items"].append(new)

                monkey["monkey business"] += 1

    monkeys = sorted(monkeys, key= lambda x: x["monkey business"], reverse=True)
    return monkeys[0]["monkey business"] * monkeys[1]["monkey business"]

def get_second_solution():
    monkeys = deepcopy(inpt_parsed)

    #Calculate lowest common denominator for tests
    tests = [monkey["test"] for monkey in monkeys]
    modulo = 1
    for test in tests:
        modulo *= test

    for j in range(10000):
        for i, monkey in enumerate(monkeys):
            while monkey["items"]:
                item = monkey["items"].pop()
                operation = monkey["operation"].split("=")[-1].strip()
                match operation.split(" "):
                    case ["old", "*", "old"]:
                        new = item*item
                    case ["old", "*", i]:
                        new = item * int(i)
                    case ["old", "+", i]:
                        new = item + int(i)

                #Discrete maths stuff, tests are still valid if value if modulo
                #divided by the common denominator of all tests
                new = new % modulo

                if new % monkey["test"] == 0:
                    next_monkey = monkey["true"]
                    monkeys[next_monkey]["items"].append(new)
                else:
                    next_monkey = monkey["false"]
                    monkeys[next_monkey]["items"].append(new)

                monkey["monkey business"] += 1

    monkeys = sorted(monkeys, key= lambda x: x["monkey business"], reverse=True)
    return monkeys[0]["monkey business"] * monkeys[1]["monkey business"]



print(get_first_solution())
print(get_second_solution())