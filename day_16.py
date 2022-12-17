from dataclasses import dataclass, field
from typing_extensions import Self
from functools import cache
import os
import re

@dataclass
class Valve:
    name: str
    flow_rate: int
    leads_to: dict[str: tuple[int, Self]] = field(default_factory=dict)

    def add_connected(self, valve: Self, distance: int):
        if valve == self:
            return
        if valve in {v for _, v in self.leads_to.values()}:
            current_distance = self.leads_to[valve.name][0]
            if distance < current_distance:
                self.leads_to[valve.name] = (distance, valve)
        else:
            self.leads_to[valve.name] = (distance, valve)

    def get_connected(self) -> list[tuple[int, Self]]:
        return list(self.leads_to.values())

    def branch_connected(self, n_iterations: int):

        for _ in range(n_iterations):
            for distance, valve in self.get_connected():
                for d, v in valve.get_connected():
                    self.add_connected(v, distance + d)

    def __repr__(self) -> str:
        leads_to = [f"{key} distance: {distance}" for key, (distance, _) in self.leads_to.items()]
        return f"Valve {self.name}, flow rate: {self.flow_rate}, leads to: {', '.join(leads_to)}"

    def __hash__(self):
        return hash(self.name)

def read_input(file_name:str) -> str:
    input_file = os.path.join(os.getcwd(), "input", f"{file_name}.txt")
    with open(input_file, 'r') as file:
        contents = [val.strip() for val in file.readlines()]

    return contents


def get_valves():
    inpt = read_input("15")

    valves: dict[str, Valve] = {}
    for row in inpt:
        name = row.partition("Valve ")[2].split(" ")[0]
        flow_rate = int(row.partition("flow rate=")[2].split(";")[0])
        valves[name] = Valve(name, flow_rate)

    for row in inpt:
        name = row.partition("Valve ")[2].split(" ")[0]
        leads_to = [valve.strip(",") for valve in re.findall("valve.? (?:.*)+", row)[0].split(" ")[1:]]

        for valve in leads_to:
            valves[name].add_connected(valves[valve], 1)

    for valve in valves.values():
        valve.branch_connected(15)

    return valves

@cache
def dfs_search(current_valve: Valve, timer: int, opened: frozenset[Valve]) -> int:
    if timer==0:
        return 0
    alternatives = []
    #Loop over connected valves plus current
    for distance, valve in current_valve.get_connected() + [(0, current_valve)]:
        #Move to an unopened valve and open it
        if (valve not in opened) and (valve.flow_rate > 0):
            if (timer - distance  - 1) > 0:
                alternatives.append((timer - distance - 1)*valve.flow_rate + dfs_search(valve, timer - distance - 1, opened | frozenset([valve])))
    if alternatives:
        return max(alternatives)
    else:
        #If all valves are opened there are no alternatives left
        return 0

valves = get_valves()

def get_first_solution():
    timer=30
    opened = frozenset()
    start = valves["AA"]
    print(timer, dfs_search(start, timer, opened))

get_first_solution()
    
