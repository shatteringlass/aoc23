import re
from util import read_input


def parse_conditions(conditions):
    pattern = re.compile(
        r"""
            (\w+)(?:([<>])(\d+):(\w+))?,?
        """, re.VERBOSE
    )

    result = []

    for condition in conditions.split(','):
        c = pattern.findall(condition)
        result.append(c[0])

    return result


def parse_workflow(workflow):
    pattern = re.compile(
        r"""(\w+) # workflow name
        \{
            (.*)
        \}
        """, re.VERBOSE)

    wfname, conditions = pattern.findall(workflow)[0]
    return wfname, parse_conditions(conditions)


def check_ratings(rtn, wkf):
    solution = 0
    end_states = ('R', 'A')
    start_state = 'in'

    for r in rtn:
        next_state = start_state
        while next_state not in end_states:
            for var, sym, val, tar in wkf[next_state]:
                if not tar:
                    next_state = var
                    break
                elif sym == '>':
                    if r[var] > int(val):
                        next_state = tar
                        break
                else:
                    if r[var] < int(val):
                        next_state = tar
                        break

        if next_state == 'A':
            solution += sum(r.values())

    return solution


def get_valid_combos(wkf, start="in", combos=None):

    if not combos:
        combos = {k: (1, 4000) for k in "xmas"}

    if start == "A":
        product = 1
        for (start, end) in combos.values():
            product *= end - start + 1
        return product

    if start == "R":
        return 0

    *rules, default = wkf[start]

    total = 0
    impossible = False

    for var, sym, num, target in rules:
        start, end = combos[var]
        num = int(num)

        if sym == '<':
            true_rng, false_rng = (start, num-1), (num, end)
        else:
            true_rng, false_rng = (num+1, end), (start, num)

        # explore true branch
        if true_rng[0] <= true_rng[1]:
            new_combos = combos.copy()
            new_combos[var] = true_rng
            total += get_valid_combos(wkf, target, new_combos)
        # update false
        if false_rng[0] <= false_rng[1]:
            combos[var] = false_rng
        else:
            impossible = True
            break

    if not impossible:
        total += get_valid_combos(wkf, default[0], combos)

    return total


def get_solution(part):

    solution = 0
    workflows, ratings = read_input('day19').split('\n\n')

    wkf = {}
    rtn = []

    for wf in workflows.splitlines():
        wfn, cond = parse_workflow(wf)
        wkf[wfn] = cond

    for r in ratings.splitlines():
        dct = {}
        for x in r[1:-1].split(','):
            k, v = x.split('=')
            dct[k] = int(v)
        rtn.append(dct)

    if part == 1:
        solution = check_ratings(rtn, wkf)

    elif part == 2:
        solution = get_valid_combos(wkf)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
