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
        for r in rtn:
            next_state = 'in'
            print(f"Assessing rating {r}")
            while next_state not in ('R', 'A'):
                for condition in wkf[next_state]:
                    print(f"Checking condition {condition}")
                    if condition[1]:
                        if condition[1] == '>':
                            if r[condition[0]] > int(condition[2]):
                                next_state = condition[3]
                                break
                        if condition[1] == '<':
                            if r[condition[0]] < int(condition[2]):
                                next_state = condition[3]
                                break
                    next_state = condition[0]

            if next_state == 'A':
                solution += sum(r.values())

    elif part == 2:
        solution = 0

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
