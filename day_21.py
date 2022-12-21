from utils import read_input
from typing import Optional, Callable

def get_monkeys() -> dict[str: int | list[str]]:
    inpt = read_input("21")
    monkeys = {}
    for row in inpt:
        monkey_name = row.split(": ")[0]
        match row.split(": ")[1].split(" "):
            case [monkey_1, operation, monkey_2]:
                monkeys[monkey_name] = [monkey_1, operation, monkey_2]
            case [number]:
                monkeys[monkey_name] = int(number)

    return monkeys

def eval_monkey(monkey_name: str, monkeys: dict[str: int | list[str]], humn_value: Optional[int] = None):
    expression = monkeys[monkey_name]
    if (monkey_name == "humn") and (humn_value is not None):
        return humn_value
    match expression:
        case [monkey_1, operation, monkey_2]:
            monkey_1_value = eval_monkey(monkey_1, monkeys, humn_value)
            monkey_2_value = eval_monkey(monkey_2, monkeys, humn_value)

            match operation:
                case '+':
                    return monkey_1_value + monkey_2_value
                case '*':
                    return monkey_1_value * monkey_2_value
                case '-':
                    return monkey_1_value - monkey_2_value
                case '/':
                    return monkey_1_value / monkey_2_value
        case number:
            return number
    return None

def binary_search(f: Callable, left_limit, right_limit):

    mid = int((right_limit + left_limit)//2)
    f_mid = f(mid)
    if f_mid == 0:
        return mid
    elif f_mid > 0:
        return binary_search(f, mid, right_limit)
    elif f_mid < 0:
        return binary_search(f, left_limit, mid)

def find_humn(monkey_name: str, monkeys: dict[str: int | list[str]]) -> bool:
    expression = monkeys[monkey_name]
    match expression:
        case [monkey_1, _, monkey_2]:
            if (monkey_1 == 'humn') or (monkey_2 == 'humn'):
                return True
            return find_humn(monkey_1, monkeys) or find_humn(monkey_2, monkeys)
        case _:
            return False

def get_first_solution(monkeys: dict[str: int | list[str]]):
    return eval_monkey("root", monkeys)

def get_second_solution(monkeys: dict[str: int | list[str]]):
    root_monkeys = [monkeys["root"][0], monkeys["root"][2]]
    humn_tree = [
        find_humn(root_monkeys[0], monkeys),
        find_humn(root_monkeys[1], monkeys),
    ]

    if humn_tree[0]:
        #Monkey in left tree, evaluate right and search left
        target = eval_monkey(root_monkeys[1], monkeys)
        f = lambda x: eval_monkey(root_monkeys[0], monkeys, x) - target

    elif humn_tree[1]:
        #Monkey in left tree, evaluate right and search left
        target = eval_monkey(root_monkeys[0], monkeys)
        f = lambda x: eval_monkey(root_monkeys[1], monkeys, x) - target

    left = 0
    right = int(1e13)
    res = binary_search(f, left, right)
    return res

print(get_first_solution(monkeys=get_monkeys()))
print(get_second_solution(monkeys=get_monkeys()))