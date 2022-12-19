from utils import read_input
from collections import deque

def get_blueprints() -> list[tuple[int, int, int, tuple[int, int], tuple[int, int]]]:
    blueprints = []
    for line in read_input("19"):
        line_split = line.split(" ")
        ore_robot_cost = int(line_split[6])
        clay_robot_cost = int(line_split[12])
        obsidian_robot_cost = (int(line_split[21]), int(line_split[18]))
        geode_robot_cost = (int(line_split[27]), int(line_split[30]))

        blueprints.append((
            clay_robot_cost,
            ore_robot_cost,
            obsidian_robot_cost,
            geode_robot_cost
        ))

    return blueprints

def solve_blueprint(
    total_time: int,
    clay_robot_cost: int,
    ore_robot_cost: int,
    obsidian_robot_cost: int,
    geode_robot_cost: int
) -> int:

    #states:
    #0: time left
    #1: clay
    #2: ore
    #3: obsidian
    #4: geode
    #5: clay robots
    #6: ore robots
    #7: obsidian robots
    #8: geode robots

    #costs:
    #clay robot cost: ore
    #ore robot cost: ore
    #obsidian robot cost: (clay, ore)
    #geode robot cost: (ore, obsidian)

    #Using a deque and popping/appending left results in a depth-first search
    queue = deque()

    initial_state = (total_time, 0, 0, 0, 0, 0, 1, 0, 0)
    queue.append(initial_state)

    max_geodes = 0
    i = 0

    while queue:
        state = queue.popleft()
        if state[0] == 0:
            #Out of time - count geodes
            if (n_geodes := state[4]) > max_geodes:
                max_geodes = n_geodes
                print(f"Iteration {i}: found new max: {max_geodes}")
                print(f"Ending state: {state}")
        else:
            costs = (
                clay_robot_cost,
                ore_robot_cost,
                obsidian_robot_cost,
                geode_robot_cost,
            )
            for next_state in get_next_states(state, *costs):

                #Theoretical max number of geodes, discard if lower than max
                max_possible_geodes = (
                    next_state[4] #Current amount
                    + next_state[8] * (next_state[0]) #Amount that will be mined
                    + sum([i for i in range(next_state[0])]) #Amount mined if one robot is built every minute
                )
                if max_possible_geodes > max_geodes:
                    queue.appendleft(next_state)
        i += 1

    return max_geodes

state_cache = {}

def get_next_states(
    state: tuple[int, ...],
    clay_robot_cost: int,
    ore_robot_cost: int,
    obsidian_robot_cost: tuple[int, int],
    geode_robot_cost: tuple[int, int]
) -> list[tuple[int, ...]]:

    clay_generated = state[5]
    ore_generated = state[6]
    obsidian_generated = state[7]
    geode_generated = state[8]

    if state[0] == 1:
        #Not worth doing anything
        #Do not cache this as this is an edge case
        return [(
            state[0] - 1,
            state[1] + clay_generated,
            state[2] + ore_generated,
            state[3] + obsidian_generated,
            state[4] + geode_generated,
            state[5],
            state[6],
            state[7],
            state[8]
        )]

    #Cache input values except for time left since no cached 
    #solution is dependent on time remaining
    cache_key = tuple([
        *state[1:],
        clay_robot_cost,
        ore_robot_cost,
        obsidian_robot_cost,
        geode_robot_cost
    ])

    if cache_key in state_cache.keys():
        return [
            (state[0] - 1, *cached_state)
            for cached_state in state_cache[cache_key]
        ]

    next_states = []

    can_build_geode_robot = (
        (state[2] >= geode_robot_cost[0]) and 
        (state[3] >= geode_robot_cost[1])
    )
    can_build_obsidian_robot = (
        (state[1] >= obsidian_robot_cost[0]) and 
        (state[2] >= obsidian_robot_cost[1])  and
        (state[7] < geode_robot_cost[1]) 
        #Only build if obsidian income is smaller than geode robot cost
    )
    can_build_clay_robot = (
        (state[2] >= clay_robot_cost) and
        (state[5] < obsidian_robot_cost[0]) 
        #Only build if clay income is smaller than clay cost for obsidian robot
    )
    can_build_ore_robot = (
        (state[2] >= ore_robot_cost) and
        (state[6] < max([ore_robot_cost, clay_robot_cost, obsidian_robot_cost[1], geode_robot_cost[0]]))
        #Only build if ore income is smaller than ore cost for any robot
    )

    if can_build_geode_robot:
        next_states.append((
            state[0] - 1,
            state[1] + clay_generated,
            state[2] - geode_robot_cost[0] + ore_generated,
            state[3] - geode_robot_cost[1] + obsidian_generated,
            state[4] + geode_generated,
            state[5],
            state[6],
            state[7],
            state[8] + 1
        ))

    else:

        if can_build_obsidian_robot:
            next_states.append((
                state[0] - 1,
                state[1] - obsidian_robot_cost[0] + clay_generated,
                state[2] - obsidian_robot_cost[1] + ore_generated,
                state[3] + obsidian_generated,
                state[4] + geode_generated,
                state[5],
                state[6],
                state[7] + 1,
                state[8]
            ))

        #Evaluate building either clay or ore robots
        if can_build_clay_robot:
            next_states.append((
                state[0] - 1,
                state[1] + clay_generated,
                state[2] - clay_robot_cost + ore_generated,
                state[3] + obsidian_generated,
                state[4] + geode_generated,
                state[5] + 1,
                state[6],
                state[7],
                state[8]
            ))

        if can_build_ore_robot:
            next_states.append((
                state[0] - 1,
                state[1] + clay_generated,
                state[2] - ore_robot_cost + ore_generated,
                state[3] + obsidian_generated,
                state[4] + geode_generated,
                state[5],
                state[6] + 1,
                state[7],
                state[8]
            ))

        #Base alternative - do nothing
        next_states.append((
            state[0] - 1,
            state[1] + clay_generated,
            state[2] + ore_generated,
            state[3] + obsidian_generated,
            state[4] + geode_generated,
            state[5],
            state[6],
            state[7],
            state[8]
        ))

    state_cache[cache_key] = [
        state[1:] for state in next_states
    ]

    return next_states

def test_solution():
    assert solve_blueprint(
                total_time=24,
                clay_robot_cost=2,
                ore_robot_cost=4,
                obsidian_robot_cost=(14,3),
                geode_robot_cost=(2,7)
            ) == 9
    assert solve_blueprint(
                total_time=24,
                clay_robot_cost=3,
                ore_robot_cost=2,
                obsidian_robot_cost=(8,3),
                geode_robot_cost=(3,12)
            ) == 12
    assert solve_blueprint(
                total_time=32,
                clay_robot_cost=2,
                ore_robot_cost=4,
                obsidian_robot_cost=(14,3),
                geode_robot_cost=(2,7)
            ) == 56
    assert solve_blueprint(
                total_time=32,
                clay_robot_cost=3,
                ore_robot_cost=2,
                obsidian_robot_cost=(8,3),
                geode_robot_cost=(3,12)
            ) == 62

def get_first_solution():
    total_quality = 0
    for i, blueprint in enumerate(get_blueprints()):
        total_quality += (
            (i + 1)
            * solve_blueprint(
                total_time=24,
                clay_robot_cost=blueprint[0],
                ore_robot_cost=blueprint[1],
                obsidian_robot_cost=blueprint[2],
                geode_robot_cost=blueprint[3]
            )
        )
    return total_quality

def get_second_solution():
    geode_product = 1
    for blueprint in get_blueprints()[:3]:
        geode_product *= solve_blueprint(
            total_time=32,
            clay_robot_cost=blueprint[0],
            ore_robot_cost=blueprint[1],
            obsidian_robot_cost=blueprint[2],
            geode_robot_cost=blueprint[3]
        )
    return geode_product


test_solution()
#print(get_first_solution())
#print(get_second_solution())