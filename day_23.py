from utils import read_input
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from collections import defaultdict
import os

class Moves(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

@dataclass
class Elf:
    position: tuple[int, int]
    planned_move: Optional[tuple[int, int]] = None

    def get_position(self) -> tuple[int, int]:
        return self.position

    def plan_move(self, direction: Moves, elf_positions: set[tuple[int, int]]) -> None:

        self.planned_move = None

        check_north = not any([(x, self.position[1] - 1) in elf_positions for x in range(self.position[0] - 1, self.position[0] + 2)])
        check_south = not any([(x, self.position[1] + 1) in elf_positions for x in range(self.position[0] - 1, self.position[0] + 2)])
        check_west = not any([(self.position[0] - 1, y) in elf_positions for y in range(self.position[1] - 1, self.position[1] + 2)])
        check_east = not any([(self.position[0] + 1, y) in elf_positions for y in range(self.position[1] - 1, self.position[1] + 2)])

        if not all([check_north, check_south, check_east, check_west]):
            for i in range(4):
                new_direction = Moves((direction.value + i)%4)

                match new_direction:
                    case Moves.NORTH:
                        if check_north:
                            self.planned_move = (self.position[0], self.position[1] - 1)
                            break
                    case Moves.SOUTH:
                        if check_south:
                            self.planned_move = (self.position[0], self.position[1] + 1)
                            break
                    case Moves.WEST:
                        if check_west:
                            self.planned_move = (self.position[0] - 1, self.position[1])
                            break
                    case Moves.EAST:
                        if check_east:
                            self.planned_move = (self.position[0] + 1, self.position[1])
                            break

    def get_planned_move(self) -> Optional[tuple[int, int]]:
        return self.planned_move

    def move(self) -> None:
        if self.planned_move is not None:
            self.position = self.planned_move
        self.planned_move = None

    def cancel_move(self) -> None:
        self.planned_move = None

def get_elves() -> list[Elf]:
    elves = []
    inpt = read_input("23")
    for y, row in enumerate(inpt):
        for x, c in enumerate(row):
            if c == "#":
                elves.append(Elf((x, y)))
    
    return elves

def print_elves(elves: list[Elf]) -> None:
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    for elf in elves:
        x, y = elf.get_position()
        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x
        if y > max_y:
            max_y = y
        if y < min_y:
            min_y = y

    grid = [["." for _ in range(min_x, max_x + 1)] for _ in range(min_y, max_y + 1)]

    for elf in elves:
        position = elf.get_position()
        grid[position[1] - min_y][position[0] - min_x] = "#"

    print(f"x: ({min_x}:{max_x}), y: ({min_y}:{max_y})")
    print("\n".join([" ".join(row) for row in grid]))

def simulate_elves(n_rounds: Optional[int] = None):
    elves = get_elves()
    directions = [
        Moves.NORTH,
        Moves.SOUTH,
        Moves.WEST,
        Moves.EAST
    ]

    i = 1
    while True:

        if n_rounds is not None:
            if i == n_rounds:
                return elves, i

        direction = directions[(i-1)%4]
        elf_positions = {elf.get_position() for elf in elves}

        move_counter = defaultdict(int)
        for elf in elves:
            elf.plan_move(direction, elf_positions)
            if (move:= elf.get_planned_move()) is not None:
                move_counter[move] += 1

        for move in [key for key, value in move_counter.items() if value > 1]:
            for elf in elves:
                if elf.get_planned_move() == move:
                    elf.cancel_move()

        for elf in elves:
            elf.move()

        if len(move_counter) == 0:
            return elves, i

        i += 1




def get_first_solution():
    elves = simulate_elves(10)[0]
    max_x = 0
    min_x = 0
    max_y = 0
    min_y = 0
    for elf in elves:
        x, y = elf.get_position()
        if x > max_x:
            max_x = x
        if x < min_x:
            min_x = x
        if y > max_y:
            max_y = y
        if y < min_y:
            min_y = y


    return (1 + max_x-min_x)*(1 + max_y-min_y) - len(elves)


def get_second_solution():
    elves, turn = simulate_elves()
    return turn

print(get_first_solution())
print(get_second_solution())