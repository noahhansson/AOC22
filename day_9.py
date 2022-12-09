from typing import Optional, Self
from utils import read_input

inpt = read_input("9")

class Knot:
    x: int
    y: int
    tail: Optional[Self]

    def __init__(self, position_x: int, position_y: int, n_children: int = 0):
        self.x = position_x
        self.y = position_y
        if n_children > 0:
            self.tail = Knot(position_x, position_y, n_children=n_children-1)
        else:
            self.tail = None

    def position(self) -> tuple[int, int]:
        return (self.x, self.y)

    def is_adjacent(self, position_x: int, position_y: int) -> bool:
        difference = (abs(self.x - position_x), abs(self.y - position_y))
        return not any([x > 1 for x in difference])

    def move(self, dx: int, dy: int) -> None:
        new_x = self.x + dx
        new_y = self.y + dy

        #If the tail is not adjecent to the head after moving, move the tail one step towards the current position
        if self.tail and not self.tail.is_adjacent(new_x, new_y):
            tail_difference = (new_x - self.tail.x, new_y - self.tail.y)
            if abs(tail_difference[0]) and abs(tail_difference[1]):
                dx = int(tail_difference[0]/abs(tail_difference[0]))
                dy = int(tail_difference[1]/abs(tail_difference[1]))
                self.tail.move(dx, dy)
            elif abs(tail_difference[0]) > 1:
                dx = int(tail_difference[0]/abs(tail_difference[0]))
                self.tail.move(dx,0)
            elif abs(tail_difference[1]) > 1:
                dy = int(tail_difference[1]/abs(tail_difference[1]))
                self.tail.move(0,dy)

        self.x = new_x
        self.y = new_y

    def get_last_tail(self) -> Self:
        if self.tail:
            return self.tail.get_last_tail()
        else:
            return self

def main(n_children: int):
    head = Knot(0, 0, n_children)

    tail_visited = set()
    tail_visited.add(head.get_last_tail().position())

    for row in inpt:
        d, n = row.split(" ")

        if d == "U":
            dx, dy = 0, -1
        elif d == "L":
            dx, dy = -1, 0
        elif d == "D":
            dx, dy = 0, 1
        elif d == "R":
            dx, dy = 1, 0

        for _ in range(int(n)):
            head.move(dx, dy)
            tail_visited.add(head.get_last_tail().position())

    return len(tail_visited)


def get_first_solution():
    return main(1)

def get_second_solution():
    return main(9)

print(get_first_solution())
print(get_second_solution())
