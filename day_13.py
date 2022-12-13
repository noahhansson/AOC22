from utils import read_input
from functools import cmp_to_key

inpt = read_input("13")

def compare_signals(pair_1, pair_2) -> bool:

    iter_left = iter(pair_1)
    iter_right = iter(pair_2)

    while ((item_left := next(iter_left, -1)) != -1) and ((item_right := next(iter_right, -1)) != -1):

        match item_left, item_right:

            case int(), int():
                #Check if left is smaller than right
                if item_left < item_right:
                    return True
                elif item_left == item_right:
                    continue
                elif item_left > item_right:
                    return False

            case list(), int():
                if (res := compare_signals(item_left, [item_right])) is not None:
                    return res 

            case int(), list():
                if (res := compare_signals([item_left], item_right)) is not None:
                    return res 

            case list(), list():
                #Compare nested objects, use recursion
                if (res := compare_signals(item_left, item_right)) is not None:
                    return res 
    else:
        if item_left != -1:
            return False
        else:
            return True

def get_first_solution():
    signal_pairs = [tuple([eval(signal) for signal in pair]) for pair in zip(inpt[::3], inpt[1::3])]
    return sum([i+1 for i, pair in enumerate(signal_pairs) if compare_signals(pair[0], pair[1])])
    

def get_second_solution():
    signals = [eval(signal) for signal in inpt if signal != ""]
    signals += [[[2]], [[6]]]
    sorted_signals = sorted(signals, key=cmp_to_key(lambda s1, s2: 1 if compare_signals(s1, s2) else -1), reverse=True)
    idx_1 = None
    idx_2 = None
    i = 0
    while (idx_1 is None) or (idx_2 is None):
        signal = sorted_signals[i]
        if signal == [[2]]:
            idx_1 = i + 1
        if signal == [[6]]:
            idx_2 = i + 1

        i+=1

    return idx_1 * idx_2

print(get_first_solution())
print(get_second_solution())