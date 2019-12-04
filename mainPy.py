import math
from typing import List
from graphics import *


def read():
    with open("data.in") as file_in:
        cnt_points = int(file_in.readline())
        points = [(0, 0)]
        for line in file_in:
            x, y = map(int, line.split())
            points.append((x, y))
        points[0] = points[cnt_points]
        points.append(points[1])
    return points, cnt_points


def sign(point_a, point_b, point_c) -> int:
    value = (point_b[0] - point_a[0]) * (point_c[1] - point_a[1]) - (point_c[0] - point_a[0]) * \
            (point_b[1] - point_a[1])
    if value == 0:
        return 0
    return 1 if value > 0 else -1


def get_polygon_orientation(points, cnt_points) -> int:
    polygon_sign = 0
    for i in range(1, cnt_points + 1):
        polygon_sign = sign(points[i - 1], points[i + 1], points[i])
        if polygon_sign != 0:
            break
    return polygon_sign


def get_points_convexity(points, cnt_points) -> List[int]:
    points_convexity = [0]
    for i in range(1, cnt_points + 1):
        points_convexity.append(sign(points[i - 1], points[i + 1], points[i]))
    return points_convexity


def distance(point_a, point_b) -> float:
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


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


def points_type(points, cnt_points) -> List[int]:
    points_principality = [0]
    for i in range(1, cnt_points + 1):
        points_principality.append(points_in_triangle(points, cnt_points, i - 1, i, i + 1))
    return points_principality


def print_points(points, cnt_points, points_convexity, points_principality):
    polygon_sign = get_polygon_orientation(points, cnt_points)
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

def graphic(points, cnt_points, convex_convexity, convex_principality):

    scale = 20; #to amke points visible (  between point(1, 1) and point(2, 4) there is brely any difference
    windowHeight = 800
    windowWidth = 1540
    pointsCpy = [Point(0, 0)]

    for i in range(1, cnt_points + 1):
        pointsCpy.append(Point(windowWidth / 2 + points[i][0] * scale,
                                                 windowHeight / 2 + points[i][1] * scale))

    c = Polygon(pointsCpy[1 : cnt_points + 1])

    win = GraphWin("Points in polygon", windowWidth, windowHeight) #set the window
    win.setCoords(0, 0, windowWidth, windowHeight)  #set the geometric reference

    inputBox = [[] for i in range(0, cnt_points + 1)]
    polygon_sign = get_polygon_orientation(points, cnt_points)

    for i in range(1, cnt_points + 1):

        if convex_principality[i] == -1 and convex_convexity[i] != polygon_sign:
            inputBox[i] = Entry(Point(pointsCpy[i].x, pointsCpy[i].y), len("Nepr|Neconv"))
            inputBox[i].setText("Nepr|Concav")

        elif convex_principality[i] == 1 and convex_convexity[i] != polygon_sign:
            inputBox[i] = Entry(Point(pointsCpy[i].x, pointsCpy[i].y), len("Pr|Neconv"))
            inputBox[i].setText("Pr|Concav")

        elif convex_principality[i] == -1 and convex_convexity[i] == polygon_sign:
            inputBox[i] = Entry(Point(pointsCpy[i].x, pointsCpy[i].y), len("Nepr|Conv"))
            inputBox[i].setText("Nepr|Convex")

        elif convex_principality[i] == 1 and convex_convexity[i] == polygon_sign:
            inputBox[i] = Entry(Point(pointsCpy[i].x, pointsCpy[i].y), len("Pr|Conv"))
            inputBox[i].setText("Pr|Convex")

        elif convex_convexity[i] == 0 or polygon_sign == 0:
            inputBox[i] = Entry(Point(pointsCpy[i].x, pointsCpy[i].y), len("Coliniare"))
            inputBox[i].setText("Coliniare")

        inputBox[i].setSize(8)

    c.setFill(color_rgb(255, 182, 203))#pink
    c.setOutline(color_rgb(199, 21, 133))
    c.draw(win) #draw the polygon lines

    for i in range(1, cnt_points + 1): #draw points labels
        inputBox[i].draw(win)

    Line(Point(windowWidth / 2, windowHeight), Point(windowWidth / 2, 0)).draw(win)  #OY
    Line(Point(0, windowHeight / 2), Point(windowWidth, windowHeight / 2)).draw(win) #OX

    oXStart = Entry(Point(20, windowHeight / 2), 4) #Ox STARTING POINT
    oXStart.setText(str(int(- windowWidth / 2 / scale)))
    oXStart.draw(win)

    oXEnd = Entry(Point(windowWidth - 20, windowHeight / 2) , 4)#Ox ENDING POINT
    oXEnd.setText(str(int(windowWidth / 2 / scale)))
    oXEnd.draw(win)

    oYStart = Entry(Point(windowWidth / 2, 15) , 4) #Oy STARTING POINT
    oYStart.setText(str(int(- windowHeight / 2 / scale)))
    oYStart.draw(win)

    oYEnd = Entry(Point(windowWidth / 2, windowHeight - 15) , 4)    #Oy ENDING POINT
    oYEnd.setText(str(int(windowHeight / 2 / scale)))
    oYEnd.draw(win)

    win.getMouse()  # Pause to view result
    win.close()  # Close window when done

def main():
    points, cnt_points = read()
    points_convexity = get_points_convexity(points, cnt_points)
    points_principality = points_type(points, cnt_points)
    print_points(points, cnt_points, points_convexity, points_principality)
    graphic(points, cnt_points, points_convexity, points_principality)

if __name__ == "__main__":
    main()

