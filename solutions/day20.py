from util import read_input
import typing
import enum
import collections


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
            return Level(sum(map(lambda x: x.value, self._state.values())))
        if self.type == ModuleType.CONJUNCTION:
            # if it remembers high pulses for all inputs, it sends a low pulse;
            if all(map(lambda x: x == Level.HI, self._state.values())):
                return Level.LOW
            # otherwise, it sends a high pulse.
            return Level.HI

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def sources(self):
        return tuple(self._state.keys())

    def receive(self, source: str, pulse: Level):
        if self.type == ModuleType.FLIPFLOP:
            if pulse == Level.LOW:
                self._state["*"] = Level(1 - self.state.value)
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
        #instr[name].state = state
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


def cycle(modules, counter=None):

    counter = counter or {Level.LOW: 1, Level.HI: 0, 'rx': False}
    left = collections.deque(['broadcaster'])

    while left:
        src = left.popleft()
        obj = modules.get(src)
        pulse = obj.state
        for d in obj.destinations:
            counter[pulse] += 1
            #print(f"{src} -{pulse}-> {d}")
            if modules[d].receive(src, pulse):
                left.append(d)

    return counter


def get_solution(part):

    solution = 0
    modules = parse_modules(read_input('day20').splitlines())

    if part == 1:
        counter = cycle(modules)
        for it in range(999):
            counter[Level.LOW] += 1
            counter = cycle(modules, counter)
        solution = counter[Level.LOW] * counter[Level.HI]
    elif part == 2:
        pass



    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
