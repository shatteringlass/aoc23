from util import read_input

i = read_input('day9').split('\n')


def diff(ls):
    n = len(ls)
    rng = range(n-1)
    return [ls[i+1] - ls[i] for i in rng]


def extrapolate(ts, side="right"):
    series = [ts]
    curr = ts

    result = 0

    while True:

        nxt = diff(curr)
        if any(nxt):
            curr = nxt
            series.append(curr)
        else:
            break

    for s in series[::-1]:
        if side == "right":
            result += s[-1]
        else:
            result = -result + s[0]

    return result


def solve(part):

    result = 0

    for line in i:
        ts = list(map(lambda x: int(x), line.split()))
        result += extrapolate(ts, side="right" if part==1 else "left")

    return result

print(f"Solution for part 1 is: {solve(1)}")
print(f"Solution for part 2 is: {solve(2)}")