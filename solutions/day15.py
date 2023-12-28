from util import read_input


def apply_hash(sequence, curval=0):

    if sequence:
        return apply_hash(sequence[1:], (17 * (curval + ord(sequence[0]))) % 256)
    return curval


def execute_step(step, boxes):
    try:
        idx = step.index('-')
        lens = step[:idx]
        box = apply_hash(lens)
        if box in boxes:
            try:
                boxes[box].pop(lens)
            except KeyError:
                pass
    except ValueError:
        lens, pwr = step.split('=')
        box = boxes.setdefault(apply_hash(lens), {})
        box[lens] = int(pwr)


def assess_power(boxes):
    pwr = 0

    for k, v in boxes.items():
        for i, (l, p) in enumerate(v.items()):
            pwr += (k+1) * (i+1) * p

    return pwr


def get_solution(part):

    solution = 0

    steps = read_input('day15').split(',')

    if part == 1:

        for step in steps:
            hashval = apply_hash(step)
            solution += hashval

    elif part == 2:

        boxes = dict()

        for step in steps:
            # print(f"Before {step}")
            # print(boxes)
            execute_step(step, boxes)
            # print(f"After {step}")
            # print(boxes)

        solution = assess_power(boxes)

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
