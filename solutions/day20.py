from util import read_input
import typing
import enum
import collections

import math


class ModuleType(enum.Enum):
    UNKNOWN = ''
    FLIPFLOP = '%'
    CONJUNCTION = '&'
    BROADCASTER = 'broadcaster'


class Level(enum.Enum):
    HI = 1
    LOW = 0


class Module:
    def __init__(self, mod_type: ModuleType, state: typing.Dict[str, Level], destinations: typing.List[str] = []):
        self.type = mod_type
        self._state = state
        self.destinations = destinations

    @property
    def state(self):
        if (self.type == ModuleType.FLIPFLOP) or (self.type == ModuleType.BROADCASTER):
            return Level(sum([v.value for k, v in self._state.items() if k != '*']))
        if self.type == ModuleType.CONJUNCTION:
            # if it remembers high pulses for all inputs, it sends a low pulse;
            # otherwise send a high pulse
            return Level(
                int(
                    Level.LOW in self._state.values()
                )
            )

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def sources(self):
        return tuple(x for x in self._state.keys() if x != '*')

    def receive(self, source: str, pulse: Level):
        if self.type == ModuleType.FLIPFLOP:
            if pulse == Level.LOW:
                self._state[self.sources[0]] = Level(1 - self.state.value)
                return True
        if self.type == ModuleType.CONJUNCTION:
            self._state[source] = pulse
            return True
        return False


def add_module(instr, src, dests):
    name, mt, state = src, ModuleType.UNKNOWN, {}

    if name == 'broadcaster':
        mt = ModuleType.BROADCASTER
        state['*'] = Level.LOW
    else:
        n, *name = name
        name = ''.join(name)
        mt = ModuleType(n)
        if mt == ModuleType.FLIPFLOP:
            state = {'*': Level.LOW}

    if name in instr:
        instr[name].type = mt
        # instr[name].state = state
        instr[name].destinations = dests
    else:
        instr[name] = Module(mt, state, dests)

    for dest in dests:
        if dest not in instr:
            instr[dest] = Module(ModuleType.UNKNOWN, {}, [])
        instr[dest]._state[name] = Level.LOW

    return instr


def parse_modules(modules):
    instr = {}

    for conn in modules:
        src, dests = conn.split(" -> ")
        instr = add_module(instr, src, [d.strip() for d in dests.split(",")])

    return instr


class ModuleLayerReachedException(Exception):

    def __init__(self, module_name):
        self.module_name = module_name


def cycle(modules, counter=None, layer=None):

    counter = counter or {Level.LOW: 0, Level.HI: 0, 'rx': False}
    left = collections.deque(['broadcaster'])

    while left:
        src = left.popleft()
        obj = modules.get(src)
        pulse = obj.state
        for d in obj.destinations:
            counter[pulse] += 1
            # print(f"{src} -{pulse}-> {d}")
            if modules[d].receive(src, pulse):
                if layer and pulse == Level.HI and d in layer:
                    raise ModuleLayerReachedException(d)
                left.append(d)

    counter[Level.LOW] += 1
    return counter


def get_solution(part):

    solution = 0
    modules = parse_modules(read_input('day20').splitlines())

    if part == 1:
        counter = None
        for _ in range(1000):
            counter = cycle(modules, counter)
        solution = counter[Level.LOW] * counter[Level.HI]
    elif part == 2:
        # Assumption #1: There is only 1 module pointing to rx
        # Assumption #2: The final module before rx is a conjunction
        # Assumption #3: The second to last layer cyclically switches to high
        cycles = []
        sources = tuple(
            s for x in modules['rx'].sources for s in modules[x].sources)
        cur_cycle = 0
        mlre = None
        while sources:
            try:
                cur_cycle += 1
                _ = cycle(modules, layer=sources)
            except ModuleLayerReachedException as mlre:
                name = mlre.module_name
                print(f"Sent HI pulse to {name}")
                sources = tuple(s for s in sources if s != name)
                cycles.append(cur_cycle)

        solution = math.lcm(*cycles)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
