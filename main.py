import math

points_convexity = []
points_principality = []


def read(points, cnt_points):
    with open("data.in") as file_in:
        cnt_points = int(file_in.readline())
        points = [(0, 0)]
        for line in file_in:
            points.append(map(int, line.split()))
        points[0] = points[cnt_points]
        points.append(points[1])


def sign(point_a, point_b, point_c) -> int:
    value = (point_b.first - point_a.first) * (point_c.second - point_a.second) - (point_c.first - point_a.first) * \
            (point_b.second - point_a.first)
    if value == 0:
        return 0
    return 1 if value > 0 else -1


def get_polygon_orientation(points, cnt_points) -> int:
    polygon_sign = 0
    for i in range(1, cnt_points + 1) and polygon_sign == 0:
        polygon_sign = sign(points[i - 1], points[i + 1], points[i])
    return polygon_sign


def get_points_convexity(points, cnt_points):
    points_convexity.append(0)
    for i in range(1, cnt_points + 1):
        points_convexity.append(sign(points[i - 1], points[i + 1], points[i]))


def distance(point_a, point_b) -> float:
    return math.sqrt((point_a.first - point_b.first) ** 2 + (point_a.second - point_b.second) ** 2)


def points_in_triangle(points, cnt_points, idx1, idx2, idx3) -> int:
    if idx1 == 0:
        idx1 = cnt_points
    if idx3 == cnt_points + 1:
        idx3 = 1

    for i in range(1, cnt_points + 1):
        if i != idx1 and i != idx2 and i != idx3:
            o1 = sign(points[idx1], points[idx2], points[i])
            o2 = sign(points[idx2], points[idx3], points[i])
            o3 = sign(points[idx3], points[idx1], points[i])

            if o1 < 0 and o2 < 0 and o3 < 0:
                return -1

            if o1 > 0 and o2 > 0 and o3 > 0:
                return -1

            if not o1 and distance(points[idx1], points[i]) + distance(points[i], points[idx2]) == distance(points[idx1], points[idx2]):
                return -1

            if not o2 and distance(points[idx2], points[i]) + distance(points[i], points[idx3]) == distance(points[idx2], points[idx3]):
                return -1

            if not o3 and distance(points[idx3], points[i]) + distance(points[i], points[idx1]) == distance(points[idx3], points[idx1]):
                return -1

    return 1


def points_type(points, cnt_points):
    points_principality.append(0)
    for i in range(1, cnt_points + 1):
        points_principality.append(points_in_triangle(points, cnt_points, i - 1, i, i + 1))


def print_points(points, cnt_points):
    polygon_sign = get_polygon_orientation()
    if polygon_sign != 0:
        for i in range(1, cnt_points + 1):
            point_sign = points_convexity[i]
            if point_sign:
                print("Varful ", end=" ")
                print(i, end=" ")
                if point_sign == polygon_sign:
                    print("convex", end=" ")
                else:
                    print("concav", end=" ")
                if points_principality[i] == 1:
                    print("principal")
                else:
                    print("neprincipal")
            else:
                print("Toate punctele sunt coliniare")
    else:
        print("Toate punctele sunt coliniare")


def main():
    cnt_points = 0
    points = []
    read(points, cnt_points)
    #get_points_convexity()
    #points_type()
    #print_points()
    print(cnt_points)


if __name__ == "__main__":
    main()

