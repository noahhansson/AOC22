from utils import read_input

inpt = read_input("15")

positions = {}

for row in inpt:
    _, _, sensor_x, sensor_y, *_, beacon_x, beacon_y = row.split(" ")
    sensor = (int(sensor_x.split("=")[1].strip(",:")),int(sensor_y.split("=")[1].strip(",:")))
    beacon = (int(beacon_x.split("=")[1].strip(",:")),int(beacon_y.split("=")[1].strip(",:")))

    positions[sensor] = beacon

def manhattan(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    '''
    Returns manhattan distance between two points
    '''

    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def get_first_solution():
    y = 2000000
    coverage = []

    for sensor, beacon in positions.items():

        if manhattan(sensor, beacon) < abs(sensor[1] - y):
            continue

        #Y-dist gives the offset from the beacon to the desired row
        y_dist = abs(sensor[1] - y)        

        width_at_y = manhattan(sensor, beacon) - y_dist

        if width_at_y > 0:
            coverage.append({
                "start": sensor[0] - width_at_y,
                "end": sensor[0] + width_at_y
            })

    coverage = sorted(coverage, key=lambda x: x["start"])
    start = coverage[0]["start"]
    end = start
    gap = 0
    for item in coverage:
        if (diff := (item["start"] - end - 1)) > 0:
            gap += diff
        if item["end"] > end:
            end = item["end"]


    return end - start - gap

def get_second_solution():
    for y in range(0, 4000000):
        coverage = []
        for sensor, beacon in positions.items():

            if manhattan(sensor, beacon) < abs(sensor[1] - y):
                continue

            #Y-dist gives the offset from the beacon to the desired row
            y_dist = abs(sensor[1] - y)        

            width_at_y = manhattan(sensor, beacon) - y_dist

            if width_at_y > 0:
                coverage.append({
                    "start": sensor[0] - width_at_y,
                    "end": sensor[0] + width_at_y
                })
    
        coverage = sorted(coverage, key=lambda x: x["start"])
        start = coverage[0]["start"]
        end = start
        for item in coverage:
            if (item["start"] - end - 1) > 0:
                if item["start"] <= 4000000:
                    target=(item["start"] - 1, y)
                    return target[0] * 4000000 + target[1]
            if item["end"] > end:
                end = item["end"]

    return None


print(get_first_solution())
print(get_second_solution())