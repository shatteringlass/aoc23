"""
Question 1:
The gardener and his team want to get started as soon as possible, 
so they'd like to know the closest location that needs a seed. 
Using these maps, find the lowest location number 
that corresponds to any of the initial seeds.
To do this, you'll need to convert each seed number through 
other categories until you can find its corresponding location number. 
What is the lowest location number that corresponds to any of the initial seed numbers?

Question 2:
Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. 
What is the lowest location number that corresponds to any of the initial seed numbers?


"""

from util import read_input

import sys

i = read_input('day5').split('\n')


def make_2uples(lst):
    return list(zip(lst[::2], lst[1::2]))


def parse_seeds():
    return sorted(map(lambda x: int(x), i[0].split(':')[1].split()))


def parse_seeds_as_rng():
    seeds = []
    toint = list(map(lambda x: int(x), i[0].split(':')[1].split()))
    tuples = sorted(make_2uples(toint))
    for (x, y) in tuples:
        seeds.append((x, x+y))
    return seeds


def parse_map_entry(entry):
    dst_start, src_start, rng_len = entry.split()
    return int(src_start), int(src_start) + int(rng_len),  int(dst_start)


def parse_maps():

    tmp = []

    for line in i[1:]:
        if not line:
            continue
        if "seed-to-soil" in line:
            continue
        elif "soil-to-fertilizer" in line:
            sts = sorted(tmp)
            tmp = []
            continue
        elif "fertilizer-to-water" in line:
            stf = sorted(tmp)
            tmp = []
            continue
        elif "water-to-light" in line:
            ftw = sorted(tmp)
            tmp = []
            continue
        elif "light-to-temperature" in line:
            wtl = sorted(tmp)
            tmp = []
            continue
        elif "temperature-to-humidity" in line:
            ltt = sorted(tmp)
            tmp = []
            continue
        elif "humidity-to-location" in line:
            tth = sorted(tmp)
            tmp = []
            continue
        else:
            tmp.append(parse_map_entry(line))

    htl = sorted(tmp)

    return sts, stf, ftw, wtl, ltt, tth, htl


def test_seed(seed, maps, current_best):

    sts, stf, ftw, wtl, ltt, tth, htl = maps

    soil = None
    fertilizer = None
    water = None
    light = None
    temperature = None
    humidity = None
    location = None

    for mapping in sts:
        if seed >= mapping[0] and seed <= mapping[1]:
            soil = mapping[2] + (seed-mapping[0])
    soil = soil or seed

    for mapping in stf:
        if soil >= mapping[0] and soil <= mapping[1]:
            fertilizer = mapping[2] + (soil-mapping[0])
    fertilizer = fertilizer or soil

    for mapping in ftw:
        if fertilizer >= mapping[0] and fertilizer <= mapping[1]:
            water = mapping[2] + (fertilizer-mapping[0])
    water = water or fertilizer

    for mapping in wtl:
        if water >= mapping[0] and water <= mapping[1]:
            light = mapping[2] + (water-mapping[0])
    light = light or water

    for mapping in ltt:
        if light >= mapping[0] and light <= mapping[1]:
            temperature = mapping[2] + (light-mapping[0])
    temperature = temperature or light

    for mapping in tth:
        if temperature >= mapping[0] and temperature <= mapping[1]:
            humidity = mapping[2] + (temperature-mapping[0])
    humidity = humidity or fertilizer

    for mapping in htl:
        if humidity >= mapping[0] and humidity <= mapping[1]:
            location = mapping[2] + (humidity-mapping[0])
    location = location or humidity

    return min(location, current_best)


def compute_solution(part):

    result = sys.maxsize
    maps = parse_maps()

    if part == 1:
        seeds = parse_seeds()
        for seed in seeds:
            result = test_seed(seed, maps, result)
    elif part == 2:
        seeds = parse_seeds_as_rng()
        for rng in seeds:
            for seed in range(rng[0], rng[1]+1):
                result = test_seed(seed, maps, result)

    return result


print(f"Solution for part 1 is: {compute_solution(1)}")
print(f"Solution for part 2 is: {compute_solution(2)}")
