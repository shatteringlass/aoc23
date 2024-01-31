import dataclasses
from util import read_input
import fractions

TEST_AREA = ((200_000_000_000_000, 200_000_000_000_000),
             (400_000_000_000_000, 400_000_000_000_000))


"""
Each stone moves along the line defined by the following parametric equation:

P(t) = P + V*t

where P is position and V is velocity.

For part 2, pick any 3 linearly independent trajectories and solve
the 6 linear equation system derived from their intersection.

"""


@dataclasses.dataclass
class Hailstone:

    position: tuple[int, int, int]
    velocity: tuple[int, int, int]

    @property
    def px(self):
        return self.position[0]

    @property
    def py(self):
        return self.position[1]

    @property
    def pz(self):
        return self.position[2]

    @property
    def vx(self):
        return self.velocity[0]

    @property
    def vy(self):
        return self.velocity[1]

    @property
    def vz(self):
        return self.velocity[2]

    def position_at_time(self, t):
        return (self.position[i] + t * self.velocity[i] for i, _ in enumerate(self.position))

    def adjust(self, frame):
        return Hailstone(self.position, tuple(c-f for c, f in zip(self.velocity, frame)))

    def intersects_xy(self, other):

        det = self.vy*other.vx - self.vx*other.vy
        if det != 0:
            t1 = (other.vx*(other.py-self.py) -
                  other.vy*(other.px-self.px))/det
            t2 = (self.vx*(other.py-self.py) - self.vy*(other.px-self.px))/det
            intersect = (t1, t2)
            # print(f"Line {self} intersects {other} at {intersect}")
        else:
            intersect = None

        return intersect

    @classmethod
    def from_str(cls, string):
        position, velocity = tuple(
            tuple(int(y) for y in x.split(',')) for x in string.split(" @ "))
        return Hailstone(position, velocity)


def find_intersection(stone, other):
    intersect = stone.intersects_xy(other)
    if intersect:
        t0, t1 = intersect
        pxt, pyt, pzt = stone.position_at_time(intersect[0])
        return ((pxt, pyt, pzt), (t0, t1))
    return None


def check_intersections(stones, min_value, max_value):
    intersections = 0

    for idx, stone in enumerate(stones):
        for jdx, other_stone in enumerate(stones[idx+1:]):
            intersection = find_intersection(stone, other_stone)
            if intersection:
                (pxt, pyt, pzt), (t0, t1) = intersection
                if t0 > 0 and t1 > 0 and (min_value <= pxt <= max_value) and (min_value <= pyt <= max_value):
                    intersections += 1

    return intersections


def check_collision_point(trajectories):
    """
    # Check whether every particle collides with the first particle in the same location
    # track the position of the collision
    collision_pos = [0, 0]

    # compare to the first particle
    i = 1

    # for each OTHER particle
    for j in 2:length(p)
        # check for a collision
        x, y, t_a, t_b = find_intersection(p[i], p[j], v[i], v[j])

        # ensure it happens in the future
        if t_a > 0 && t_b > 0
            # for the first collision, just update the value
            if collision_pos == [0, 0]
                collision_pos = [x, y]

            # otherwise, ensure both the x and y match and if not, return a failure
            elseif !all([x, y] .≈ collision_pos)
                return [0, 0]
            end
        end
    end
    # on success return the position that everything collided at
    return collision_pos
    """
    return


def find_z(rock, trajectories):
    z, t = [], []
    for i in range(3):
        stone = trajectories[i]
        intersection = find_intersection(rock, stone)
        if intersection:
            (pxt, pyt, pzt), (t0, t1) = intersection
            z.append(t1*stone.velocity[2]+stone.position[2])
            t.append(t1)

    """
    # convert those into z velocities
    vz_s = diff(z) ./ diff(t)

    # if there are all the same (i.e. matches a straight line - celebration time)
    if all(vz_s .≈ vz_s[1])
        # get the launch velocity and position of the z coordinate
        vz = round(vz_s[1])
        z = round(p[3][3] + t[3] * (v[3][3] - vz))
        return (z, vz)
    else
        # otherwise this one is a bust
        return (0, 0)
    end
    """
    return


def find_perfect_shot(trajectories, xy_range=(-500, 500)):

    for vx in range(xy_range[0], xy_range[1]):
        for vy in range(xy_range[0], xy_range[1]):
            rock_vel = (0, 0, 0), (vx, vy, 0)
            adjusted_trajectories = [h.adjust(rock_vel) for h in trajectories]

            launch_pos = check_collision_point(adjusted_trajectories)

            if launch_pos == (0, 0):
                continue

            z, vz = find_z(
                Hailstone(launch_pos, rock_vel),
                adjusted_trajectories
            )

            if vz == 0:
                continue

            return sum(launch_pos) + z


def get_solution(part):

    solution = 0
    data = read_input('day24').splitlines()

    stones = tuple(Hailstone.from_str(line) for line in data)

    if part == 1:
        solution = check_intersections(
            stones, TEST_AREA[0][0], TEST_AREA[1][1])
    elif part == 2:
        pass

    return solution


def main():
    print(f"Solution for part 1 is: {get_solution(1)}")
    print(f"Solution for part 2 is: {get_solution(2)}")


if __name__ == '__main__':
    main()
