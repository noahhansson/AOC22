from dataclasses import dataclass, field
from utils import read_input
from typing import Self
from functools import cache
from itertools import combinations
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

        self.leads_to = {key: value for key, value in self.leads_to.items() if value[1].flow_rate > 0}

    def __repr__(self) -> str:
        return f"Valve {self.name}"

    def __hash__(self):
        return hash(self.name)


def get_valves() -> dict[str, Valve]:
    inpt = read_input("16")

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

    valves = {key: valve for key, valve in valves.items() if (valve.flow_rate > 0) or (key=="AA")}

    return valves

@cache
def dfs_search(current_valve: Valve, timer: int, opened: frozenset[Valve], required: frozenset[Valve]) -> int:
    if timer==0:
        return 0
    alternatives = []
    #Loop over connected valves plus current
    for distance, valve in current_valve.get_connected() + [(0, current_valve)]:
        #Move to an unopened valve and open it
        if (valve not in opened) and (valve.flow_rate > 0) and (valve in required):
            if (timer - distance  - 1) > 0:
                alternatives.append((timer - distance - 1)*valve.flow_rate + dfs_search(valve, timer - distance - 1, opened | frozenset([valve]), required))
    if alternatives:
        return max(alternatives)
    else:
        #If all valves are opened there are no alternatives left
        return 0

valves = get_valves()

def get_first_solution():
    timer=30
    opened = frozenset()
    required = frozenset(valves.values())
    start = valves["AA"]
    return dfs_search(start, timer, opened, required)

def get_second_solution():
    timer=26
    opened = frozenset()
    scores = []
    for r in range(len(valves) // 2):
        for items in combinations(valves.values(), r):
            required_1 = frozenset(items)
            required_2 = frozenset(set(valves.values()) - required_1)

            start = valves["AA"]
            score = dfs_search(start, timer, opened, required_1) + dfs_search(start, timer, opened, required_2)
            scores.append(score)

    return max(scores)

print(get_first_solution())
print(get_second_solution())
