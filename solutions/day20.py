from util import read_input
import typing
import enum
import collections


class ModuleType(enum.Enum):
    FLIPFLOP = '%'
    CONJUNCTION = '&'
    BROADCASTER = ''


class Level(enum.Enum):
    HI = 1
    LOW = 0


class Module:
    def __init__(self, type: ModuleType, state: typing.Dict[str, Level], source: str = None, destinations: typing.List[str] = []):
        self.type = type
        self.state = state
        self.source = source
        self.destinations = destinations

    @property
    def state(self):
        if (self.type == ModuleType.FLIPFLOP) or (self.type == ModuleType.BROADCASTER):
            return Level(sum(self.state.values()))
        if self.type == ModuleType.CONJUNCTION:
            return Level(int(not all(self.state.values)))

    def add_source(self, src_name):
        if self.type == ModuleType.CONJUNCTION:
            self.state[src_name] = Level.LOW

    def receive(self, source: str, pulse: Level):
        if self.type == ModuleType.FLIPFLOP:
            self.state["*"] = Level(1 - self.state.value)
        if self.type == ModuleType.CONJUNCTION:
            self.state[source] = pulse


""" 
class FlipFlopModule(Module):
    def __init__(self):
        super().__init__(0)

    @property
    def output(self):
        return self.state

    def receive(self, src, pulse):
        if (pulse == 0):
            self.state = 1 - self.state


class ConjunctionModule(Module):
    def __init__(self, inputs={}):
        super().__init__(inputs)

    @property
    def output(self):
        print(f"Input state: {self.state}")
        return int(not all(self.state))

    def add_input(self, src, pulse=0):
        self.state[src] = pulse

    def receive(self, src, pulse):
        self.add_input(src, pulse)


class BroadcastModule(Module):
    def __init__(self):
        super().__init__(0)

    @property
    def output(self):
        return self.state

    def receive(self, src, pulse):
        self.state = pulse
 """


def get_module(src):
    if src == 'broadcaster':
        return src, Module(ModuleType.BROADCASTER, 0)
    if '%' in src:
        return src[1:], Module(ModuleType.FLIPFLOP, 0)
    if '&' in src:
        return src[1:], Module(ModuleType.CONJUNCTION, 0)
    return src, Module({})


def parse_modules(modules):
    config = {}

    for module in modules:
        src, dests = module.split(" -> ")
        src_name, obj = get_module(src)
        src_config = config.setdefault(src_name, (obj, []))

        for d in dests.split(","):
            dest_name, dest_obj = get_module(d.strip())

            if dest_name not in config:
                # destination not yet created
                config[dest_name] = (dest_obj, [])
            else:
                # destination present
                prev_dest_obj = config[dest_name][0]
                _, this_dest_obj = get_module(dest_name)
                if isinstance(this_dest_obj, Module):
                    # Generic module
                    if isinstance(prev_dest_obj, Module):
                        # Specific module type still unknown
                        continue
                    else:
                        # Specific module type already known
                        continue
                else:
                    # not a generic module
                    if isinstance(prev_dest_obj, Module):
                        # convert the old type into the new
                        config[dest_name][0] = this_dest_obj
                        this_dest_obj.state = prev_dest_obj.state
                    else:
                        # this case cannot really happen
                        print("Found double definition for module")

            config[dest_name][0].add_input(src_name)
            src_config[1].append(dest_name)

    return config


def cycle(modules):
    print(modules)
    counter = {0: 1, 1: 0}
    left = collections.deque(modules.keys())

    while left:
        src = left.popleft()
        obj, dests = modules.get(src)
        print(f"Calculating output for {src}")
        pulse = obj.output
        for d in dests:
            counter[pulse] += 1
            print(f"{src} -{pulse}-> {d}")
            if d in modules:
                modules[d][0].receive(src, pulse)
                left.append(d)

    return counter


def get_solution(part):

    solution = 0
    modules = parse_modules(read_input('day20_small2').splitlines())

    if part == 1:
        print(cycle(modules))
    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
